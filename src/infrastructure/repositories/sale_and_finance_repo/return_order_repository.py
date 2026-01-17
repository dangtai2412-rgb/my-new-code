from infrastructure.models.sale_and_finance.return_order_model import ReturnOrderModel
from infrastructure.databases import session

class ReturnOrderRepository:
    def add(self, return_order):
        session.add(return_order)
        session.commit()
        return return_order

    def get_all(self, owner_id):
        return session.query(ReturnOrderModel)\
                      .filter_by(owner_id=owner_id)\
                      .order_by(ReturnOrderModel.return_date.desc())\
                      .all()