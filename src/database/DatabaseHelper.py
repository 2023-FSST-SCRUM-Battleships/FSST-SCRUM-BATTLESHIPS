"""
DatabaseHelper is a module that provides a set of tools to facilitate
working with MySQL databases using Peewee.

Classes:
    BaseModel: a base class for all models/database to inherit from.
    DatabaseHelper: a class that provides helper methods for managing
                    database connections and transactions.

Usage:
    To use DatabaseHelper, import the module and create a new instance of
    the DatabaseHelper class. Use the instance's methods to connect to a
    database, start a transaction, and execute queries.

Example:
    from DatabaseHelper import DatabaseHelper, BaseEntity
    from peewee import *

    class Person(BaseEntity):
        name = CharField()
        age = IntegerField()

    db = DatabaseHelper()
    db.connect()
    db.update_schema()

    with db.transaction():
        # create a new person record
        person = Person.create(name='Alice', age=25)

        # retrieve all people from the database
        people = Person.select()

    db.close()
"""
import pymysql

from peewee import *

import database

_host = "localhost"
_user = "battleships"
_database = "battleships"
_password = "(Dsi@!WQqc3VC8ztD=n/(:rg)u9VmFN["
_db = MySQLDatabase(host=_host, user=_user, database=_database, password=_password)


class BaseEntity(Model):
    """
    Base Entity for all database/models to inherit from
    It simply pre-sets Meta-data for peewee
    use _strinclude to auto-include the supplied attributes in the __str__ method
    """

    def __str__(self):
        # magic make funny string :)
        if hasattr(self, "_strinclude"):
            attributes = [f"{attr}={getattr(self, attr)}" for attr in getattr(self, "_strinclude")]
            return f"{self.__class__.__name__}(id={self.id}, {attributes})"
        return f"{self.__class__.__name__}(id={self.id})"

    class Meta:
        """
        Meta-data for peewee
        """
        database = _db


class DatabaseHelper(object):
    def connect(self):
        conn = pymysql.connect(host=_host, user=_user, password = _password)
        conn.cursor().execute(f'CREATE DATABASE IF NOT EXISTS `{_database}`')
        conn.close()
        _db.connect(True)

    def update_schema(self):
        _db.create_tables(BaseEntity.__subclasses__())

    def close(self):
        _db.close()

    def transaction(self, *args, **kwargs):
        return _db.transaction(*args, **kwargs)