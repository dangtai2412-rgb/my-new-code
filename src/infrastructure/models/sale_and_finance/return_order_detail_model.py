from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base

class ReturnOrderDetailModel(Base):
    __tablename__ = 'return_order_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    return_id = Column(Integer, ForeignKey('return_orders.return_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    
    quantity = Column(Integer, nullable=False)     # Số lượng trả
    refund_price = Column(Numeric(12, 2), default=0) # Giá hoàn lại (thường bằng giá bán lúc mua)

    return_order = relationship("ReturnOrderModel", back_populates="details")
    product = relationship("ProductModel")