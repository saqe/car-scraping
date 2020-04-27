import mysql.connector

class MySQLDBHandler:
    def __init__(self,_host_,_user_,_passwd_,_database_):
        super().__init__()
        self.db_connection=mysql.connector.connect(
            host=_host_,
            user=_user_,
            passwd=_passwd_,
            database=_database_)
        self.db_cursor=self.db_connection.cursor()

        print("Connection built with database! ver: ",self.db_connection.get_server_info())

    def is_connected(self) -> bool:
        return self.db_connection.is_connected()
    
    def query(self,sql_query) -> None:
        self.db_cursor.execute(sql_query)

    def insert_qeury(self,sql_query) -> None:
        self.db_cursor.execute(sql_query)
        self.db_connection.commit()

    def fetch_many(self,sql_query) -> list:
        self.db_cursor.execute(sql_query)
        return self.db_cursor.fetchall()
    
    def fetch_many_first(self,sql_query) -> list:
        self.db_cursor.execute(sql_query)
        return [x[0] for x in self.db_cursor.fetchall()]

    def fetch_one(self,sql_query) -> tuple:
        self.db_cursor.execute(sql_query)
        return self.db_cursor.fetchone()
        

        

