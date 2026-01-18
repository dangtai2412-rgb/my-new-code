from flask import Blueprint, jsonify
from sqlalchemy import func
from datetime import datetime, timedelta

# Import trực tiếp database và model (Không dùng Service/Container nữa)
from infrastructure.databases import session
from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel
from infrastructure.models.inventory.product_model import ProductModel
from infrastructure.models.sale_and_finance.expense_model import ExpenseModel
from api.middlewares.auth_middleware import token_required

# Tạo Blueprint
account_report_bp = Blueprint('account_report_bp', __name__)

# --- 1. API DASHBOARD (Thống kê tổng quan) ---
@account_report_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard_stats(current_user):
    try:
        # Lấy ID chủ shop từ token
        owner_id = getattr(current_user, 'owner_id', None)
        today = datetime.now().date()
        month_start = today.replace(day=1)

        # 1. Doanh thu hôm nay (Chỉ tính đơn đã trả tiền)
        revenue_today = session.query(func.sum(OrderModel.total_amount))\
            .filter(
                OrderModel.owner_id == owner_id,
                func.date(OrderModel.created_at) == today,
                OrderModel.payment_status == 'PAID'
            ).scalar() or 0

        # 2. Số đơn hàng hôm nay
        orders_today = session.query(func.count(OrderModel.order_id))\
            .filter(
                OrderModel.owner_id == owner_id,
                func.date(OrderModel.created_at) == today
            ).scalar() or 0

        # 3. Sản phẩm sắp hết (Dưới 10 cái)
        low_stock_count = session.query(func.count(ProductModel.product_id))\
            .filter(
                ProductModel.owner_id == owner_id,
                ProductModel.stock_quantity < 10
            ).scalar() or 0

        # 4. Chi phí tháng này
        expenses_month = session.query(func.sum(ExpenseModel.amount))\
            .filter(
                ExpenseModel.owner_id == owner_id,
                func.date(ExpenseModel.expense_date) >= month_start
            ).scalar() or 0

        return jsonify({
            "revenue_today": float(revenue_today),
            "orders_today": orders_today,
            "low_stock_count": low_stock_count,
            "expenses_month": float(expenses_month)
        }), 200
    except Exception as e:
        print(f"Lỗi Dashboard: {e}")
        return jsonify({"message": str(e)}), 500


# --- 2. API CHART (Biểu đồ doanh thu 7 ngày) ---
@account_report_bp.route('/chart', methods=['GET'])
@token_required
def get_chart_data(current_user):
    try:
        owner_id = getattr(current_user, 'owner_id', None)
        data = []
        
        # Chạy vòng lặp 7 ngày gần nhất
        for i in range(6, -1, -1):
            date_check = datetime.now().date() - timedelta(days=i)
            total = session.query(func.sum(OrderModel.total_amount))\
                .filter(
                    OrderModel.owner_id == owner_id,
                    func.date(OrderModel.created_at) == date_check,
                    OrderModel.payment_status == 'PAID'
                ).scalar() or 0
            
            data.append({
                "date": date_check.strftime("%d/%m"),
                "revenue": float(total)
            })
        return jsonify(data), 200
    except Exception as e:
        print(f"Lỗi Chart: {e}")
        return jsonify([]), 200


# --- 3. API TOP PRODUCTS (Sản phẩm bán chạy) ---
@account_report_bp.route('/top-products', methods=['GET'])
@token_required
def get_top_products(current_user):
    try:
        owner_id = getattr(current_user, 'owner_id', None)
        
        # Join bảng: Product -> OrderDetail -> Order
        results = session.query(
            ProductModel.product_name,
            func.sum(OrderDetailModel.quantity)
        ).join(OrderDetailModel, ProductModel.product_id == OrderDetailModel.product_id)\
         .join(OrderModel, OrderDetailModel.order_id == OrderModel.order_id)\
         .filter(ProductModel.owner_id == owner_id)\
         .group_by(ProductModel.product_name)\
         .order_by(func.sum(OrderDetailModel.quantity).desc())\
         .limit(5).all()
        
        return jsonify([{"name": r[0], "sold": r[1]} for r in results]), 200
    except Exception as e:
        print(f"Lỗi Top Product: {e}")
        return jsonify([]), 200