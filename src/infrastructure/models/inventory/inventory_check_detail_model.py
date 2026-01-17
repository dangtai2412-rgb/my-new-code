from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base

class InventoryCheckDetailModel(Base):
    __tablename__ = 'inventory_check_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    check_id = Column(Integer, ForeignKey('inventory_checks.check_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    
    system_quantity = Column(Integer) # Tồn kho trên phần mềm lúc kiểm
    actual_quantity = Column(Integer) # Tồn kho thực tế đếm được
    # difference = actual - system (Hệ thống tự tính hoặc lưu cũng được)

    inventory_check = relationship("InventoryCheckModel", back_populates="details")
    product = relationship("ProductModel")