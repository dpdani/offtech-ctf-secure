#!/bin/bash

echo "Backup started at $(date +'%I:%M')" >> /tmp/backup.log

mkdir -p /tmp/database_backups
sudo mysqldump --defaults-extra-file=/root/db_config.cnf --single-transaction --databases ctf2 > /tmp/database_backups/backup_db_$(date +"%H_%M").sql
cd /tmp/database_backups
ls -tr | head -n -5 | xargs rm  # it keeps only the most 5 recent backup in the folder
