from sqlalchemy import func, and_
from datetime import datetime, timedelta
from infrastructure.databases import session
from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel
from infrastructure.models.sale_and_finance.expense_model import ExpenseModel
from infrastructure.models.inventory.product_model import ProductModel

class AccountReportService:
    def __init__(self, account_report_repository):
        self.repo = account_report_repository

    def get_dashboard_stats(self, owner_id):
        """Lấy số liệu thống kê cho Dashboard"""
        today = datetime.now().date()
        
        # 1. Tính doanh thu hôm nay
        revenue_today = session.query(func.sum(OrderModel.total_amount))\
            .filter(
                OrderModel.owner_id == owner_id,
                func.date(OrderModel.created_at) == today,
                OrderModel.payment_status == 'PAID'
            ).scalar() or 0

        # 2. Đếm số đơn hôm nay
        orders_today = session.query(func.count(OrderModel.order_id))\
            .filter(
                OrderModel.owner_id == owner_id,
                func.date(OrderModel.created_at) == today
            ).scalar() or 0

        # 3. Sản phẩm sắp hết hàng (Giả sử < 10 là cảnh báo)
        low_stock_count = session.query(func.count(ProductModel.product_id))\
            .filter(
                ProductModel.owner_id == owner_id,
                ProductModel.stock_quantity <= 10
            ).scalar() or 0

        # 4. Tính tổng chi phí tháng này
        current_month = datetime.now().month
        expenses_month = session.query(func.sum(ExpenseModel.amount))\
            .filter(
                ExpenseModel.owner_id == owner_id,
                func.extract('month', ExpenseModel.expense_date) == current_month
            ).scalar() or 0

        return {
            "revenue_today": float(revenue_today),
            "orders_today": orders_today,
            "low_stock_count": low_stock_count,
            "expenses_month": float(expenses_month)
        }

    def get_revenue_chart(self, owner_id):
        """Lấy dữ liệu biểu đồ doanh thu 7 ngày gần nhất"""
        data = []
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
        return data

    def get_top_products(self, owner_id):
        """Lấy top 5 sản phẩm bán chạy nhất"""
        results = session.query(
            ProductModel.product_name,
            func.sum(OrderDetailModel.quantity).label('total_sold')
        ).join(OrderDetailModel, ProductModel.product_id == OrderDetailModel.product_id)\
         .join(OrderModel, OrderDetailModel.order_id == OrderModel.order_id)\
         .filter(ProductModel.owner_id == owner_id)\
         .group_by(ProductModel.product_name)\
         .order_by(func.sum(OrderDetailModel.quantity).desc())\
         .limit(5).all()

        return [{"name": r[0], "sold": r[1]} for r in results]