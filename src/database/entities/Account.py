from peewee import CharField, IntegerField
from database import BaseEntity


class Account(BaseEntity):
    username = CharField()
    password = CharField()
    win_count = IntegerField()
    loss_count = IntegerField()
    _strinclude = ["username"]
