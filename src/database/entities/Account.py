from peewee import CharField, IntegerField

from database import BaseEntity


class Account(BaseEntity):
    username = CharField()
    password_hash = CharField()
    win_count = IntegerField()
    loss_count = IntegerField()
    _strinclude = ["username"]