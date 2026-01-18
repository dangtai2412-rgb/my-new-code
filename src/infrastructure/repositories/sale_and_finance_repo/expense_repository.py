from infrastructure.models.sale_and_finance.expense_model import ExpenseModel
from infrastructure.databases import session

class ExpenseRepository:
    def add(self, expense):
        session.add(expense)
        session.commit()
        return expense

    def get_all(self, owner_id):
        return session.query(ExpenseModel)\
                      .filter_by(owner_id=owner_id)\
                      .order_by(ExpenseModel.expense_date.desc())\
                      .all()
    
    def delete(self, expense_id):
        # Tìm và xóa (để làm tính năng xóa phiếu chi nếu nhập sai)
        expense = session.query(ExpenseModel).filter_by(expense_id=expense_id).first()
        if expense:
            session.delete(expense)
            session.commit()
            return True
        return False