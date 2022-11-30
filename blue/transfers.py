import pymysql as sql
def deposit(usr,amount:int):
    db=sql.connect('localhost','root','rootmysql','ctf2')
    cursor=db.cursor()
    cursor.execute("UPDATE transfers SET amount=amount+'%d' WHERE user='%s'" % (amount,usr))
    db.commit()
    db.close()
def withdraw(usr,amount:int):
    db=sql.connect('localhost','root','rootmysql','ctf2')
    cursor=db.cursor()
    try:
        cursor.execute("UPDATE transfers SET amount=amount-'%d' WHERE user='%s'" % (amount,usr))
        db.commit()
    except:
        print("insufficient funds!")    
    db.close()