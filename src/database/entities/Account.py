from peewee import CharField, IntegerField

from database import BaseEntity


class Account(BaseEntity):
    username = CharField()
    password_hash = CharField()

    _strinclude = ["username"]