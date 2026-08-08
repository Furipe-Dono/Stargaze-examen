import os
import pymysql.cursors


class MySQLConnection:

    def __init__(self, db):

        self.connection = pymysql.connect(
            host=os.getenv("MYSQLHOST", "localhost"),
            user=os.getenv("MYSQLUSER", "root"),
            password=os.getenv("MYSQLPASSWORD", "root"),
            database=os.getenv("MYSQLDATABASE", db),
            port=int(os.getenv("MYSQLPORT", 3306)),
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):

        if data is None:
            data = {}

        try:
            with self.connection.cursor() as cursor:

                query = cursor.mogrify(query, data)

                print("Running Query:", query)

                cursor.execute(query)

                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid

                elif query.lower().find("select") >= 0:
                    return cursor.fetchall()

                else:
                    self.connection.commit()
                    return None

        except Exception as e:
            print("Something went wrong:", e)
            return False

        finally:
            self.connection.close()


def connectToMySQL(db):
    return MySQLConnection(db)