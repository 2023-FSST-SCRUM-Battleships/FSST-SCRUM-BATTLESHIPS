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
        try:
            user = Account.get_or_none(name=name, password=password)
            # TODO: pop up message: Successful login in or simply game start
        except Account.DoesNotExist:
            # TODO: pop up message: Sorry, we couldn't find an account with that name and password
            self.create_account(name, password)

    def create_account(self, name, password):

        with self.db.transaction():
            user = Account.get_or_none(name=name)
            if user:
                return False
            # TODO: GUI message -> Sorry, that username is already taken
            # TODO: repeat sign up in GUI and call create_account function
            # self.create_account(username, pass)

            user = Account.create(name=name, password=password)
            user.save()
            # TODO: GUI message -> Account created successfully!

    def close(self):
        self.db.close()
