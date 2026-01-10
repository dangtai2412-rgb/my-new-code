from infrastructure.models.inventory.stock_import_model import StockImportModel
from infrastructure.models.inventory.stock_import_detail_model import StockImportDetailModel
from datetime import datetime

class StockImportService:
    def __init__(self, repository):
        self.repository = repository

    def create_stock_import(self, data, owner_id):
        # 1. Tạo Header cho phiếu nhập
        new_import = StockImportModel(
            owner_id=owner_id,
            supplier_id=data['supplier_id'],
            import_date=datetime.now(),
            total_amount=0
        )

        details = []
        final_total = 0

        # 2. Xử lý danh sách sản phẩm nhập về
        if 'items' in data:
            for item in data['items']:
                qty = int(item['quantity'])
                price = float(item['unit_price'])
                line_total = qty * price
                
                detail = StockImportDetailModel(
                    product_id=item['product_id'],
                    quantity=qty,
                    unit_price=price,
                    line_total=line_total
                )
                details.append(detail)
                final_total += line_total

        # 3. Gán danh sách và tổng tiền
        new_import.details = details
        new_import.total_amount = final_total

        return self.repository.add_import_with_details(new_import)
    def get_history_by_owner(self, owner_id):
        # Repository cần có hàm get_by_owner
        return self.repository.get_by_owner(owner_id)