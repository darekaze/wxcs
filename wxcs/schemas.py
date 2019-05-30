"""Schema file."""
from marshmallow import Schema, fields


class CaseSchema(Schema):
    """The Case schema."""

    id = fields.Int(dump_only=True)
    codename = fields.Str(dump_only=True)
    title = fields.Str()
    start_at = fields.DateTime()
    end_at = fields.DateTime()
    log = fields.Str(dump_only=True)
    description = fields.Str()
