from infrastructure.models.inventory.stock_import_detail_model import StockImportDetailModel

class StockImportDetailService:
    def __init__(self, repository):
        self.repository = repository

    def create_detail(self, data):
        # Tính toán line_total nếu cần (mặc dù model hiện tại chưa có cột này, 
        # nhưng thường dùng để trả về cho Frontend)
        quantity = int(data['quantity'])
        unit_price = float(data['unit_price'])
        
        new_detail = StockImportDetailModel(
            import_id=data['import_id'],
            product_id=data['product_id'],
            quantity=quantity,
            unit_price=unit_price
        )
        return self.repository.add(new_detail)

    def get_details_by_import(self, import_id):
        return self.repository.get_by_import_id(import_id)