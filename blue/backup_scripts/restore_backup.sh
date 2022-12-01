#!/bin/bash

BACKUP=${1:?"Specify the path of the backup as argv[1]"}

sudo mysql --defaults-extra-file=~/offtech-ctf-secure/blue/backup_scripts/db_config.cnf < $BACKUP
