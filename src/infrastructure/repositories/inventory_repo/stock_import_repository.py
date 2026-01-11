from infrastructure.models.inventory.stock_import_model import StockImportModel
from infrastructure.models.inventory.stock_import_detail_model import StockImportModel
from infrastructure.models.inventory.product_model import ProductModel
from infrastructure.databases.mssql import session

class StockImportRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    def add_import_with_details(self, import_model):
        try:
            self.session.add(import_model)
            
            # LOGIC QUAN TRỌNG: Duyệt qua từng dòng hàng để tăng tồn kho
            for detail in import_model.details:
                product = self.session.query(ProductModel).filter_by(product_id=detail.product_id).first()
                if product:
                    # Cộng thêm số lượng nhập vào tồn kho hiện tại
                    product.stock_quantity += detail.quantity 
                
            self.session.commit()
            self.session.refresh(import_model)
            return import_model
        except Exception as e:
            self.session.rollback()
            raise e
    def get_by_owner(self, owner_id):
        """Lấy danh sách phiếu nhập hàng của một chủ shop"""
        return self.session.query(StockImportModel).filter_by(owner_id=owner_id).all()
    