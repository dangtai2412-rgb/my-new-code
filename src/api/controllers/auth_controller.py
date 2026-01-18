from flask import Blueprint, jsonify
from sqlalchemy import func
from datetime import datetime, timedelta

# Import trực tiếp (Không qua Container để tránh lỗi)
from infrastructure.databases import session
from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel
from infrastructure.models.inventory.product_model import ProductModel
from infrastructure.models.sale_and_finance.expense_model import ExpenseModel
from api.middlewares.auth_middleware import token_required

account_report_bp = Blueprint('account_report_bp', __name__)

@account_report_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard_stats(current_user):
    try:
        owner_id = getattr(current_user, 'owner_id', None)
        today = datetime.now().date()
        month_start = today.replace(day=1)

        revenue_today = session.query(func.sum(OrderModel.total_amount))\
            .filter(OrderModel.owner_id == owner_id, func.date(OrderModel.created_at) == today, OrderModel.payment_status == 'PAID').scalar() or 0

        orders_today = session.query(func.count(OrderModel.order_id))\
            .filter(OrderModel.owner_id == owner_id, func.date(OrderModel.created_at) == today).scalar() or 0

        low_stock_count = session.query(func.count(ProductModel.product_id))\
            .filter(ProductModel.owner_id == owner_id, ProductModel.stock_quantity < 10).scalar() or 0

        expenses_month = session.query(func.sum(ExpenseModel.amount))\
            .filter(ExpenseModel.owner_id == owner_id, func.date(ExpenseModel.expense_date) >= month_start).scalar() or 0

        return jsonify({
            "revenue_today": float(revenue_today),
            "orders_today": orders_today,
            "low_stock_count": low_stock_count,
            "expenses_month": float(expenses_month)
        }), 200
    except Exception as e:
        print(f"Lỗi Dashboard: {e}")
        return jsonify({"message": "Lỗi lấy dữ liệu dashboard"}), 500

@account_report_bp.route('/chart', methods=['GET'])
@token_required
def get_chart_data(current_user):
    return jsonify([]), 200 # Trả về rỗng tạm thời để không lỗi

@account_report_bp.route('/top-products', methods=['GET'])
@token_required
def get_top_products(current_user):
    return jsonify([]), 200 # Trả về rỗng tạm thời