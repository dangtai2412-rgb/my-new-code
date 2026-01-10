class UnitService:
    def __init__(self, repository):
        self.repository = repository

    def create_unit(self, data):
        # Kiểm tra logic cơ bản
        if not data.get('product_id'):
            raise ValueError("product_id là bắt buộc")
        if not data.get('unit_name'):
            raise ValueError("Tên đơn vị không được để trống")

        return self.repository.add(
            product_id=data['product_id'], 
            name=data['unit_name'], 
            rate=data.get('conversion_rate', 1), 
            is_base=data.get('is_base_unit', False)
        )

    # BỔ SUNG: Hàm lấy danh sách đơn vị theo sản phẩm
    def get_units_by_product(self, product_id):
        return self.repository.get_by_product(product_id)
    def delete_unit(self, unit_id):
        return self.repository.delete(unit_id)