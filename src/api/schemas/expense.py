from marshmallow import Schema, fields

class ExpenseSchema(Schema):
    expense_id = fields.Int(dump_only=True)
    expense_name = fields.Str(required=True)
    amount = fields.Float(required=True)
    expense_date = fields.DateTime(dump_only=True) # Hoặc cho phép nhập nếu muốn nhập bù
    category = fields.Str(required=True)
    note = fields.Str(allow_none=True)