from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base

class OrderDetailModel(Base):
    __tablename__ = 'order_details'

    # 1. Thêm ForeignKey kết nối với bảng Orders
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True, nullable=False)
    
    # 2. Thêm ForeignKey kết nối với bảng Products
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True, nullable=False)
    
    # (Nếu có unit_id cũng nên thêm ForeignKey luôn)
    unit_id = Column(Integer, ForeignKey('units.unit_id'), nullable=True)

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    
    # --- THÊM RELATIONSHIP ĐỂ CODE PYTHON DỄ GỌI ---
    order = relationship("OrderModel", back_populates="details")
    product = relationship("ProductModel", back_populates="order_details")
    unit = relationship("UnitModel") # Để lấy tên đơn vị (Cái/Thùng/Hộp)