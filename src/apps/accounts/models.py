from tortoise import models, fields


class Account(models.Model):
    id = fields.IntField(pk=True)
    fullname = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
