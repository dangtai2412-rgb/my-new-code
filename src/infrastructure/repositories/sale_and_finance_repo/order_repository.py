from infrastructure.models.sale_and_finance.order_model import OrderModel
from infrastructure.models.inventory.product_model import ProductModel
from infrastructure.databases.mssql import session

class OrderRepository:
    def __init__(self, db_session=session):
        self.session = db_session

    
    def add_order_with_details(self, order_model):
        """Lưu hóa đơn và TỰ ĐỘNG TRỪ KHO"""
        try:
            self.session.add(order_model)
            # Duyệt qua từng sản phẩm trong đơn hàng
            for detail in order_model.details:
                product = self.session.query(ProductModel).filter_by(product_id=detail.product_id).first()
                if product:
                    # Kiểm tra tồn kho trước khi bán
                    stock = product.stock_quantity or 0
                    if stock < detail.order_quantity:
                        raise ValueError(f"Sản phẩm {product.product_name} không đủ hàng! (Kho: {stock}, Cần: {detail.order_quantity})")
                    
                    # Trừ số lượng trong kho
                    product.stock_quantity = stock - detail.order_quantity
            
            self.session.commit()
            self.session.refresh(order_model)
            return order_model
        except Exception as e:
            self.session.rollback()
            raise e