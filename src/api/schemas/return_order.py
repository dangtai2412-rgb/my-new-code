from marshmallow import Schema, fields

class ReturnOrderDetailSchema(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    refund_price = fields.Float(required=True) # Giá hoàn tiền cho mỗi món

class ReturnOrderSchema(Schema):
    return_id = fields.Int(dump_only=True)
    return_code = fields.Str(dump_only=True)
    customer_id = fields.Int(required=True)
    order_id = fields.Int(allow_none=True)
    return_date = fields.DateTime(dump_only=True)
    total_refund = fields.Float(dump_only=True)
    reason = fields.Str()
    details = fields.List(fields.Nested(ReturnOrderDetailSchema), required=True)