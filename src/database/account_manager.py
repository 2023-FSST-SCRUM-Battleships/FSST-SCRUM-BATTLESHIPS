from src.database.DatabaseHelper import DatabaseHelper
from src.database.entities.Account import Account


class AuthHelper(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = DatabaseHelper()
        self.db.connect()
        self.db.update_schema()

    def check_credentials(self, name, password):
        # name, password comes from GUI
        return Account.get_or_none(username=name, password=password)

    def create_account(self, name, password):
        with self.db.transaction():
            user = Account.get_or_none(username=name)
            # username is already taken
            if user:
                return None
            else:
                user = Account.create(username=name, password=password)
                user.save()
                return user

    def close(self):
        self.db.close()
