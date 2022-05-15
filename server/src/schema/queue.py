
from marshmallow import Schema, fields


class QueueSchema(Schema):
    id_lot = fields.Str()
    id_buyer = fields.Str()
    data = fields.Str()