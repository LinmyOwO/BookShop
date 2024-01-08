class DBManager:
    def __init__(self, db_connection):
        self.__db = db_connection
        self.__cur = db_connection.cursor()