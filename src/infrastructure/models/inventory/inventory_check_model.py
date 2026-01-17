from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.databases.base import Base

class InventoryCheckModel(Base):
    __tablename__ = 'inventory_checks'

    check_id = Column(Integer, primary_key=True, autoincrement=True)
    check_code = Column(String(50), unique=True, nullable=False) # Mã phiếu: IC001
    check_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='DRAFT') # DRAFT (Nháp), COMPLETED (Đã cân bằng)
    note = Column(String(255))
    
    owner_id = Column(Integer, ForeignKey('business_owners.owner_id'))
    
    # Quan hệ
    details = relationship("InventoryCheckDetailModel", back_populates="inventory_check", cascade="all, delete-orphan")