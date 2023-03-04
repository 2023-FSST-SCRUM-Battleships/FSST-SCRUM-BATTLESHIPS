from peewee import CharField, IntegerField

from database import BaseEntity


class SignUpToken(BaseEntity):
    uuid = CharField()
    _strinclude = ["uuid"]