import mysql.connector
from lang import lang

class Dbc:
    def __init__(self):
        self.db =  mysql.connector.connect(
            host="localhost",
            user="jasur",
            password="J@$Ur",
            database="qr_bot"
        )
        
    def select(self, query:str, value:tuple = None):
        try:
            cursor = self.db.cursor()
            if value:
                cursor.execute(query, value)
            else:
                cursor.execute(query)
            ans = cursor.fetchall()
            cursor.close()
            return ans
        except:
            print("Error on selecting ", query, value)
            return []
    def insert(self, query:str, value:tuple):
        try:
            cursor = self.db.cursor()
            cursor.execute(query, value)
            self.db.commit()
            ans = cursor.rowcount
            cursor.close()
            return ans
        except:
            print("Error on insering ", query, value)
            return 0
    
    def select_one(self, query:str, value:tuple = None) -> dict:
        try:
            fields = []
            d_fields = dict()
            cursor = self.db.cursor()
            if value:
                cursor.execute(query, value)
            else:
                cursor.execute(query)

            for i in cursor.description:
                fields.append( i[0] )

            ans = cursor.fetchall()

            if ans != []:
                for i in range(len(fields)):
                    d_fields[fields[i]] = ans[0][i]
            
            cursor.close()
            return d_fields
        except:
            print("Error on selecting ", query, value)
            return {}
    def select_many(self, query:str, value:tuple = None) -> list:
        try:
            result = []
            fields = []
            cursor = self.db.cursor()
            if value:
                cursor.execute(query, value)
            else:
                cursor.execute(query)

            for i in cursor.description:
                fields.append( i[0] )

            ans = cursor.fetchall()

            for row in ans:
                d_fields = dict()
                for i in range(len(fields)):
                    d_fields[fields[i]] = row[i]
                result.append(d_fields)
            
            cursor.close()
            return result
        except:
            print("Error on selecting ", query, value)
            return {}



database = Dbc()


