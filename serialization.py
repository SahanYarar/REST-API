from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(validate=validate.Length(max=20))
    email = fields.Email(validate=validate.Length(max=120))
    is_admin = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class AccountSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=validate.Length(max=20))
    user_id = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
