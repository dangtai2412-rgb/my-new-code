from marshmallow import Schema, fields

class CategorySchema(Schema):
    category_id = fields.Int(dump_only=True)
    category_name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    owner_id = fields.Int(dump_only=True)