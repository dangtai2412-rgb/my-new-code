from marshmallow import Schema, fields
from api.schemas.order_detail import OrderDetailSchema

class OrderSchema(Schema):
    order_id = fields.Int(dump_only=True)
    order_code = fields.Str(dump_only=True)
    
    # Thông tin khách hàng
    customer_id = fields.Int(required=True)
    customer_name = fields.Str(dump_only=True) # Nếu muốn hiện tên khách
    
    # Thông tin đơn hàng
    total_amount = fields.Float(dump_only=True)
    payment_status = fields.Str(dump_only=True)
    order_status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    
    # Danh sách chi tiết sản phẩm (Nested)
    # Lưu ý: Cần file order_detail.py có class OrderDetailSchema
    details = fields.List(fields.Nested(OrderDetailSchema), dump_only=True)