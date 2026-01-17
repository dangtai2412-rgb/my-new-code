from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.databases.base import Base

class ReturnOrderModel(Base):
    __tablename__ = 'return_orders'

    return_id = Column(Integer, primary_key=True, autoincrement=True)
    return_code = Column(String(50), unique=True, nullable=False) # Mã phiếu: RO-123
    
    # Có thể trả hàng từ đơn cũ hoặc trả tự do
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    
    return_date = Column(DateTime, default=datetime.utcnow)
    total_refund = Column(Numeric(12, 2), default=0) # Tổng tiền hoàn lại
    reason = Column(String(255)) # Lý do trả: Dư dùng, Hàng lỗi...
    
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'))

    # Quan hệ
    details = relationship("ReturnOrderDetailModel", back_populates="return_order", cascade="all, delete-orphan")
    customer = relationship("CustomerModel")
    