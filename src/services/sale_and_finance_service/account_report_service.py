from sqlalchemy import func
from datetime import datetime, timedelta
from infrastructure.databases import session
from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel
from infrastructure.models.inventory.product_model import ProductModel
from infrastructure.models.sale_and_finance.expense_model import ExpenseModel

class AccountReportService:
    # 👇 Chú ý: tên biến là repository
    def __init__(self, repository):
        self.repo = repository

    def get_dashboard_stats(self, owner_id):
        today = datetime.now().date()
        month_start = today.replace(day=1)
        
        # Logic tính toán
        revenue_today = session.query(func.sum(OrderModel.total_amount))\
            .filter(OrderModel.owner_id == owner_id, func.date(OrderModel.created_at) == today, OrderModel.payment_status == 'PAID').scalar() or 0

        orders_today = session.query(func.count(OrderModel.order_id))\
            .filter(OrderModel.owner_id == owner_id, func.date(OrderModel.created_at) == today).scalar() or 0

        low_stock_count = session.query(func.count(ProductModel.product_id))\
            .filter(ProductModel.owner_id == owner_id, ProductModel.stock_quantity < 10).scalar() or 0

        expenses_month = session.query(func.sum(ExpenseModel.amount))\
            .filter(ExpenseModel.owner_id == owner_id, func.date(ExpenseModel.expense_date) >= month_start).scalar() or 0

        return {
            "revenue_today": float(revenue_today),
            "orders_today": orders_today,
            "low_stock_count": low_stock_count,
            "expenses_month": float(expenses_month)
        }

    def get_revenue_chart(self, owner_id):
        data = []
        for i in range(6, -1, -1):
            date_check = datetime.now().date() - timedelta(days=i)
            total = session.query(func.sum(OrderModel.total_amount))\
                .filter(OrderModel.owner_id == owner_id, func.date(OrderModel.created_at) == date_check, OrderModel.payment_status == 'PAID').scalar() or 0
            data.append({"date": date_check.strftime("%d/%m"), "revenue": float(total)})
        return data

    def get_top_products(self, owner_id):
        results = session.query(ProductModel.product_name, func.sum(OrderDetailModel.quantity))\
         .join(OrderDetailModel, ProductModel.product_id == OrderDetailModel.product_id)\
         .join(OrderModel, OrderDetailModel.order_id == OrderModel.order_id)\
         .filter(ProductModel.owner_id == owner_id)\
         .group_by(ProductModel.product_name).order_by(func.sum(OrderDetailModel.quantity).desc()).limit(5).all()
        return [{"name": r[0], "sold": r[1]} for r in results]