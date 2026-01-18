class Product:
    def __init__(self, product_name, owner_id, cost_price=0, selling_price=0, stock_quantity=0, product_id=None):
        self.product_id = product_id
        self.product_name = product_name
        self.owner_id = owner_id        # Khóa ngoại nối đến BusinessOwner
        self.selling_price = selling_price
        self.stock_quantity = stock_quantity
        self.cost_price = cost_price