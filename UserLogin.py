from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, user_id, db_table):
        self.__user = db_table.query.get(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user.id)

    def get_name(self):
        return str(self.__user.username)
