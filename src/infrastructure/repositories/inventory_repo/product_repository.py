from infrastructure.models.inventory.product_model import ProductModel
from domain.models.product import Product
from infrastructure.databases.mssql import session

class ProductRepository:
    def __init__(self, db_session=session):
        # Sử dụng session từ mssql.py làm mặc định
        self.session = db_session

    def add(self, prod: Product):
        """
        Thêm sản phẩm mới vào database.
        Chuyển đổi dữ liệu từ lớp Domain (Product) sang Database Model (ProductModel).
        """
        try:
            db_prod = ProductModel(
                product_name=prod.product_name,
                owner_id=prod.owner_id,
                selling_price=prod.selling_price,
                stock_quantity=prod.stock_quantity
            )
            self.session.add(db_prod)
            self.session.commit()
            self.session.refresh(db_prod) # Lấy lại ID tự động tăng từ DB
            return db_prod
        except Exception as e:
            self.session.rollback()
            raise e

    def get_all(self):
        """
        Lấy toàn bộ danh sách sản phẩm trong hệ thống.
        """
        return self.session.query(ProductModel).all()

    def get_by_owner(self, owner_id: int):
        """
        Lấy danh sách sản phẩm thuộc về một chủ doanh nghiệp cụ thể.
        Hàm này PHẢI CÓ để khớp với ProductService.
        """
        return self.session.query(ProductModel).filter_by(owner_id=owner_id).all()

    def get_by_id(self, product_id: int):
        """
        Tìm kiếm một sản phẩm cụ thể theo ID.
        """
        return self.session.query(ProductModel).filter_by(product_id=product_id).first()
    def get_by_id(self, product_id):
        """Lấy 1 sản phẩm theo ID"""
        return self.session.query(ProductModel).filter_by(product_id=product_id).first()

    def update(self, product_model):
        """Lưu các thay đổi của sản phẩm"""
        try:
            self.session.commit()
            return product_model
        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, product_id):
        """Xóa sản phẩm"""
        try:
            product = self.get_by_id(product_id)
            if product:
                self.session.delete(product)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise e