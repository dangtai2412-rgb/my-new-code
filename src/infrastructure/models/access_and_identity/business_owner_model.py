from sqlalchemy import Column, Integer, String, ForeignKey
from infrastructure.databases.base import Base
from sqlalchemy.orm import relationship
class BusinessOwnerModel(Base):
    __tablename__ = 'business_owners'
    #__table_args__ = {'extend_existing': True}

    owner_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_name = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    email = Column(String(100))
    account_status = Column(String(20))
    # Khóa ngoại nối đến Admin
    admin_id = Column(Integer, ForeignKey('administrators.admin_id'))
    
    password = Column(String(255), nullable=False)
    plan_id = Column(Integer, ForeignKey('subscription_plans.plan_id'))
    
    