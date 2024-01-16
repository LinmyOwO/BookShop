from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, user_id, db_table):
        self.__user = db_table.query.get(user_id)
        self.__cart = []
        return self

    def create(self, user):
        self.__user = user
        self.__cart = []
        return self

    def add_to_cart(self, book):
        if book not in self.__cart:
            self.__cart.append(book)

    def delete_from_cart(self, book):
        if book in self.__cart:
            self.__cart.remove(book)

    def is_book_in_cart(self, book):
        return book in self.__cart

    def get_id(self):
        return str(self.__user.id)

    def get_cart(self):
        return self.__cart

    def clear_cart(self):
        self.__cart = []