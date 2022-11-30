from hashlib import sha256
import random
from random import shuffle
import hashlib
random.seed(69)
def shuffle_word(word):
 word = list(word)
 shuffle(word)
 return ''.join(word)
def SHA256(message):
    return sha256(message.encode()).hexdigest()
def signup (usere, passwd):
  db_user=['a','b','c','d']#here we should update it everytime a new user is created
  db_pass=[]#here too
  salt_list=[12,13,23,45]#here a different random number for each user
  if usere in db_user:
    print("username already exists")
    return 1
  else:
    db_user.append(usere)
    new_salt=random.randint(100000000,999999999)
    new_salt=SHA256(str(new_salt))[0:10]
    salt_list.append(new_salt)
    password=shuffle_word(passwd)
    password=password+new_salt
    hashed = hashlib.md5(password.encode())
    peppered="42scb7b112aa"+hashed.hexdigest()
    db_pass.append(peppered)
    
    print(peppered)

