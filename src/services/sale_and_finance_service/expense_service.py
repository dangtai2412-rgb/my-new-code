from infrastructure.models.sale_and_finance.expense_model import ExpenseModel

class ExpenseService:
    def __init__(self, expense_repository):
        self.expense_repository = expense_repository

    def create_expense(self, data, owner_id):
        new_expense = ExpenseModel(
            expense_name=data['expense_name'],
            amount=data['amount'],
            category=data.get('category', 'Khác'),
            note=data.get('note', ''),
            owner_id=owner_id
        )
        return self.expense_repository.add(new_expense)

    def get_expenses(self, owner_id):
        return self.expense_repository.get_all(owner_id)

    def delete_expense(self, expense_id):
        return self.expense_repository.delete(expense_id)