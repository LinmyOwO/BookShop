class DBManager:
    def __init__(self, dbConnection):
        self.__db = dbConnection
        self.__cur = dbConnection.cursor()

    def getBookInfo(self, bookid):
        sqlRequest = f"SELECT * FROM book WHERE id == {bookid}"
        try:
            self.__cur.execute(sqlRequest)
            bookInfo = self.__cur.fetchone()
            return bookInfo
        except:
            print("Ошибка чтения из БД")
        return None
