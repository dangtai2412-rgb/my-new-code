from marshmallow import Schema, fields

class OrderDetailSchema(Schema):
    product_id = fields.Int(required=True)
    product_name = fields.Str(dump_only=True) # Hiện tên sản phẩm cho dễ nhìn
    quantity = fields.Int(required=True)
    unit_price = fields.Float(dump_only=True)
    total_price = fields.Float(dump_only=True)