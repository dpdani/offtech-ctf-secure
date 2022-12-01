from hashlib import sha256
from random import shuffle
import hashlib
import mysql.connector
import sys

def shuffle_word(word):
 word = list(word)
 shuffle(word)
 return ''.join(word)
def SHA256(message):
    return sha256(message.encode()).hexdigest()
def login(users,passwd):
    db = mysql.connector.connect(user='script', password='ude2z&YU3Mq!LR#!%h#e', host='localhost', database='ctf2')
    cursor=db.cursor()
    cursor.execute("SELECT user FROM users WHERE user='%s'" % (users))
    check1=cursor.fetchone()
    if users!=check1[0]:
        db.close()
        return False
    else:
        cursor.execute("SELECT pass FROM users WHERE user='%s'" % (users))
        pas=cursor.fetchone() 
        cursor.execute("SELECT salt FROM users WHERE user='%s'" % (users))
        salt=cursor.fetchone()
        new_pass=passwd+salt[0]
        hashed = hashlib.md5(new_pass.encode())
        peppered="42scb7b112aa"+hashed.hexdigest()
        if peppered==pas[0]:
            db.close()
            return True
        elif peppered!=pas[0]:
            db.close()
            return False

if __name__ == "__main__":
    print(login(sys.argv[1], sys.argv[2]))
