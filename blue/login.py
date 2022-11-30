from hashlib import sha256
import random
from random import shuffle
import hashlib
import pymysql as sql
random.seed(69)
def shuffle_word(word):
 word = list(word)
 shuffle(word)
 return ''.join(word)
def SHA256(message):
    return sha256(message.encode()).hexdigest()
def login(users,passwd):
    db=sql.connect('localhost','root','rootmysql','ctf2')
    cursor=db.cursor()
    cursor.execute("SELECT user FROM users WHERE user='%s'" % (users))
    check1=cursor.fetchone()
    if users!=check1:
        db.close()
        return False
    else:
        cursor.execute("SELECT pass FROM users WHERE user='%s'" % (users))
        pas=cursor.fetchone() 
        cursor.execute("SELECT salt FROM users WHERE user='%s'" % (users))
        salt=cursor.fetchone()
        new_pass=passwd+salt
        hashed = hashlib.md5(new_pass.encode())
        peppered="42scb7b112aa"+hashed.hexdigest()
        if peppered==pas:
            db.close()
            return True
        elif peppered!=pas:
            db.close()
            return False