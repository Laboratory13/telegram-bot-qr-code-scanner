import mysql.connector
from lang import lang

class Dbc:
    def __init__(self):
        self.db =  mysql.connector.connect(
            host="localhost",
            user="jasur",
            password="J@$Ur",
            database="tg_bot"
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


database = Dbc()


def get_lang(user_id:int, def_lan:str = "en", set_defaul:bool = False):
    quer = "SELECT * FROM lang WHERE id = %s"
    val = (user_id, )
    ans = database.select(quer, val)
    if set_defaul:
        return lang.gl(def_lan)
    if ans == []:
        quer = "INSERT INTO lang (id, lang) VALUES (%s, %s)"
        val = (user_id, def_lan)
        ans2 = database.insert(quer, val)
        if ans2 == 0:
            print("Error!" + " #15")
        return lang.gl(def_lan)
    return lang.gl(str(ans[0][1]))

def get_lang_str(user_id:int, def_lang:str):
    quer = "SELECT * FROM lang WHERE id = %s"
    val = (user_id, )
    ans = database.select(quer, val)
    if ans == []:
        return def_lang
    return str(ans[0][1])

def calc_admin(admin:int):
    quer = "SELECT SUM(rate) AS rate_sum, COUNT(*) AS rate_count FROM `finished` WHERE admin_id = %s"
    val = (admin, )
    ans = database.select_one(quer, val)
    if ans == {}:
        return -1
    else:
        if ans["rate_count"] == 0:
            return 0
        else:
            quer = "UPDATE admins SET con_count = %s, avg_rate = %s WHERE admin_id = %s"
            val = (ans["rate_count"], ans["rate_sum"] / ans["rate_count"], admin)
            ans2 = database.insert(quer, val)
            if ans2 == 0:
                return -1
            else:
                return 0

