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
def signup (usere, passwd):
    db=sql.connect('localhost','root','rootmysql','ctf2')
    cursor=db.cursor()
    new_salt=random.randint(1,999999999)
    new_salt=SHA256(str(new_salt))[0:10]
    #password=shuffle_word(passwd)
    password=passwd+new_salt
    hashed = hashlib.md5(password.encode())
    peppered="42scb7b112aa"+hashed.hexdigest()
    command="INSERT INTO users(user,pass,salt) VALUES ( '%s','%s','%s')" % (usere,peppered,new_salt)
    command2="INSERT INTO transfers(user) VALUES ( '%s')" % (usere)
    cursor.execute(command)
    db.commit()
    cursor.execute(command2)
    db.commit()
    db.close()