"""Schema file."""
from marshmallow import Schema, fields
from enum import Enum


class CaseSchema(Schema):
    """The Case schema."""

    id = fields.Int(dump_only=True)
    codename = fields.Str(dump_only=True)
    title = fields.Str()
    start_at = fields.DateTime()
    end_at = fields.DateTime()
    log = fields.Str(dump_only=True)
    description = fields.Str()


class LinkSchema(Schema):
    """The Link schema."""

    id = fields.Int(dump_only=True)
    name = fields.Str()
    href = fields.Str(dump_only=True)
    icon = fields.Str()
    ctg = fields.Int()
    interval_min = fields.Int()
    base_min = fields.Int()
    post = fields.Str()


class LinkEnum(Enum):
    """Enum of Link."""

    Uncategorized = 0
    Observations = 1
    Prognoses = 2
    Operations = 3
    Others = 4
