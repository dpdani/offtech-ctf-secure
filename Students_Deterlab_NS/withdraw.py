import mysql.connector
import sys

def withdraw(usr,amount:int):
    db = mysql.connector.connect(user='root', password='rootmysql', host='localhost', database='ctf2')
    cursor=db.cursor()
    try:
        cursor.execute("insert into transfers (user, amount, tstamp) values ('%s', '%d', now())" % (usr, amount))
        db.commit()
    except:
        print("insufficient funds!")    
    db.close()

if __name__ == "__main__":
    print(withdraw(sys.argv[1], sys.argv[2]))