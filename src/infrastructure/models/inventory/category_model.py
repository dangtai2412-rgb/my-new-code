from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base

class CategoryModel(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100), nullable=False)
    description = Column(String(255))
    
    # Một danh mục thuộc về 1 chủ shop
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'))

    # Quan hệ 1-nhiều: Một danh mục có nhiều sản phẩm
    products = relationship("ProductModel", back_populates="category")