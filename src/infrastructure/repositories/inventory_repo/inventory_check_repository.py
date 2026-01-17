from infrastructure.models.inventory.inventory_check_model import InventoryCheckModel
from infrastructure.models.inventory.inventory_check_detail_model import InventoryCheckDetailModel
from infrastructure.databases import session

class InventoryCheckRepository:
    def add(self, inventory_check):
        """Lưu phiếu kiểm kho vào DB"""
        session.add(inventory_check)
        session.commit()
        return inventory_check

    def add_detail(self, detail):
        """Lưu chi tiết phiếu kiểm"""
        session.add(detail)
        # Không commit ngay để đảm bảo transaction (commit 1 lần ở Service)
    
    def get_all_by_owner(self, owner_id):
        """Lấy lịch sử kiểm kho của Shop"""
        return session.query(InventoryCheckModel)\
                      .filter_by(owner_id=owner_id)\
                      .order_by(InventoryCheckModel.check_date.desc())\
                      .all()

    def get_by_code(self, code):
        return session.query(InventoryCheckModel).filter_by(check_code=code).first()