from marshmallow import Schema, fields

from src.utils import must_not_be_blank


class LotSchema(Schema):
    id = fields.Int(dump_only=True)
    id_author = fields.Str() # UserSchema(only=('id'))
    name = fields.Str(validate=must_not_be_blank)
    description = fields.Str()
    price = fields.Str(validate=must_not_be_blank)
    date_time = fields.Str()