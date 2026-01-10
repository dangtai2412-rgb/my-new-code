from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.sale_and_finance.order_detail_model import OrderDetailModel

from infrastructure.models.sale_and_finance.account_report_model import AccountReportModel
from infrastructure.databases.mssql import session

class AccountReportRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add(self, report_model):
        try:
            self.session.add(report_model)
            self.session.commit()
            self.session.refresh(report_model)
            return report_model
        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_owner(self, owner_id):
        return self.session.query(AccountReportModel).filter_by(owner_id=owner_id).all()
    
    
    def get_revenue_data(self, start_date, end_date):
        """
        Truy vấn dữ liệu từ bảng Orders và OrderDetails để đổ vào mẫu S1-HKD
        """
        return self.session.query(
            OrderModel.order_date,
            OrderModel.order_id,
            OrderDetailModel.order_quantity,
            OrderDetailModel.unit_price,
            OrderDetailModel.line_total,
            # Giả định bạn có thêm trường category hoặc product_name
        ).join(OrderDetailModel, OrderModel.order_id == OrderDetailModel.order_id)\
         .filter(OrderModel.order_date >= start_date)\
         .filter(OrderModel.order_date <= end_date)\
         .all()