from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from datetime import datetime
from infrastructure.databases.base import Base

class ExpenseModel(Base):
    __tablename__ = 'expenses'

    expense_id = Column(Integer, primary_key=True, autoincrement=True)
    expense_name = Column(String(255), nullable=False) # VD: Tiền điện tháng 1
    amount = Column(Numeric(12, 2), nullable=False)    # Số tiền chi
    expense_date = Column(DateTime, default=datetime.utcnow)
    category = Column(String(100)) # VD: Điện nước, Mặt bằng, Lương...
    note = Column(String(255))
    
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'))