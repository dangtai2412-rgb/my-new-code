from domain.models.product import Product

class ProductService:
    def __init__(self, repository):
        # repository ở đây chính là ProductRepository từ infrastructure
        self.repository = repository

    def create_product(self, data):
        # 1. Kiểm tra logic (ví dụ giá không được âm)
        price = float(data.get('selling_price', 0))
        stock = int(data.get('stock_quantity', 0))
        cost = float(data.get('cost_price', 0))
        if price < 0:
            raise ValueError("Giá bán không được nhỏ hơn 0")

        # 2. Đóng gói dữ liệu vào đối tượng Product (Domain)
        product_domain = Product(
            product_name=data.get('product_name'),
            owner_id=data.get('owner_id'),
            selling_price=price,
            cost_price=cost,
            stock_quantity=data.get('stock_quantity', 0)
        )

        # 3. Gọi Repository để lưu vào DB
        return self.repository.add(product_domain)

    def get_all_products(self):
        return self.repository.get_all()
    # ... các hàm cũ giữ nguyên ...
    

    def get_products_by_owner(self, owner_id):
    # Sửa get_all() thành get_by_owner(owner_id)
        return self.repository.get_by_owner(owner_id)
    def update_product(self, product_id, data):
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValueError("Không tìm thấy sản phẩm")
        
        # Cập nhật các trường
        product.product_name = data.get('product_name', product.product_name)
        product.selling_price = float(data.get('selling_price', product.selling_price))
        product.stock_quantity = int(data.get('stock_quantity', product.stock_quantity))
        
        return self.repository.update(product)

    def delete_product(self, product_id):
        return self.repository.delete(product_id)
    