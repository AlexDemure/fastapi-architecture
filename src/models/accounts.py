from tortoise import fields, models

from src.enums.accounts import AccountType


class Account(models.Model):
    id = fields.IntField(pk=True)
    fullname = fields.CharField(max_length=128, null=False)
    account_type = fields.CharEnumField(AccountType, max_lenght=64, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
