import mysql.connector
import sys

def deposit(usr,amount:int):
    db = mysql.connector.connect(user='root', password='rootmysql', host='localhost', database='ctf2')
    cursor=db.cursor()
    cursor.execute("insert into transfers (user, amount, tstamp) values ('%s', '%d', now())" % (usr, -amount))
    db.commit()
    db.close()

if __name__ == "__main__":
    print(deposit(sys.argv[1], sys.argv[2]))