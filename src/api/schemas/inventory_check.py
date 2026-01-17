from marshmallow import Schema, fields

class InventoryCheckDetailSchema(Schema):
    product_id = fields.Int(required=True)
    system_quantity = fields.Int(dump_only=True) # Chỉ xuất ra, không nhập vào
    actual_quantity = fields.Int(required=True)  # Số thực tế đếm được

class InventoryCheckSchema(Schema):
    check_id = fields.Int(dump_only=True)
    check_code = fields.Str(dump_only=True)
    check_date = fields.DateTime(dump_only=True)
    status = fields.Str(dump_only=True)
    note = fields.Str()
    details = fields.List(fields.Nested(InventoryCheckDetailSchema), required=True)