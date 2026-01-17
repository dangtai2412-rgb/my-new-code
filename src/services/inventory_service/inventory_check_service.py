from datetime import datetime
from infrastructure.models.inventory.inventory_check_model import InventoryCheckModel
from infrastructure.models.inventory.inventory_check_detail_model import InventoryCheckDetailModel
from infrastructure.databases import session 

# ❌ ĐÃ XÓA dòng import dependency_container và wiring (Nguyên nhân gây lỗi)

class InventoryCheckService:
    # ❌ ĐÃ XÓA @inject (Không cần thiết vì Container đã tự động tiêm rồi)
    def __init__(
        self, 
        product_repository,         # Chỉ cần khai báo biến
        inventory_check_repository  # Container sẽ tự truyền vào đây
    ):
        self.product_repository = product_repository
        self.inventory_check_repository = inventory_check_repository

    def create_check(self, data, owner_id):
        # 1. Tạo phiếu cha
        code = f"IC-{int(datetime.now().timestamp())}"
        new_check = InventoryCheckModel(
            check_code=code,
            note=data.get('note', ''),
            owner_id=owner_id,
            status='COMPLETED'
        )
        session.add(new_check)
        session.flush() # Lấy ID

        # 2. Duyệt từng sản phẩm để xử lý
        for item in data['details']:
            product = self.product_repository.get_by_id(item['product_id'])
            
            # Nếu sản phẩm không tồn tại hoặc không phải của chủ shop này -> Bỏ qua
            if not product or product.owner_id != owner_id: 
                continue

            # Lưu chi tiết kiểm
            detail = InventoryCheckDetailModel(
                check_id=new_check.check_id,
                product_id=product.product_id,
                system_quantity=product.stock_quantity, # Lưu lại số cũ
                actual_quantity=item['actual_quantity'] # Lưu số mới
            )
            session.add(detail)

            # 🚀 QUAN TRỌNG: Cập nhật kho về đúng số thực tế
            product.stock_quantity = item['actual_quantity']
        
        # 3. Lưu tất cả vào DB
        session.commit()
        return new_check
    
    def get_history(self, owner_id):
        return self.inventory_check_repository.get_all_by_owner(owner_id)