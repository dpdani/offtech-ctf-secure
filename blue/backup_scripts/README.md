## Database backups

To make a manual database backup run:

```console
sudo ./backup_db.sh
```

The backup will be saved in `/tmp/database_backups` in the format `backup_db_minute_second.sql`. Note that the script keeps only the 5 most recent backups.

To start a `cron job` that will automatically do the backup every 5 minutes use:

```console
./start_automatic_backup.sh
```

To change the frequency of the backups edit `/etc/crontab`.

To restore a backup run:

```console
./restore_backup.sh <path-to-the-backup>
```
