## README - Atlassian Scripts ##

These scripts can be used on the Library's Confluence, JIRA and Crowd servers for the purpose of managing back-ups, restores and creating new test/production environments

### What these scripts do ###

* atlassian_create_test_server : Creates a Confluence, JIRA or Crowd test server given the back-up files of a production server
```

Usage: atlassian_create_test_server [ -c | -j | -w ] -d [DATABASE-HOSTNAME] -x [PATH-TO-CFGXML-FILE] -s [PATH-TO-SQLDUMP-FILE] -i [PATH-TO-INSTALLDIR-TAR] -h [PATH-TO-HOMEDIR-TAR]
-c        --> Create a Confluence test server
-j        --> Create a JIRA test server
-w        --> Create a Crowd test server
-d DATABASE-HOSTNAME      --> Hostname of MySQL Database server
-x PATH-TO-CFGXML-FILE    --> Location of xml file with connection information to the Confluence/JIRA Test database
-s PATH-TO-SQLDUMP-FILE   --> Location of the Production SQL DUMP file
-i PATH-TO-INSTALLDIR-TAR --> Location of the Production Installation directory archive
-h PATH-TO-HOMEDIR-TAR    --> Location of the Production Home directory archive
```
* atlassian_db_backup : Perform a Confluence, JIRA or Crowd database backup
```

Usage: atlassian_db_backup [ -c | -j | -w ] [ -s ]
-c --> Backup Confluence MySQL DB
-j --> Backup JIRA MySQL DB
-w --> Backup Crowd MySQL DB
-s --> Indicate this script should run in silent mode
```
* atlassian_drop_db_tables : Drops all tables from the specified database - this is used during restore operations to ensure a clean database
```

Usage: atlassian_drop_db_tables <DBNAME>
```
* atlassian_fs_backup : Performs a Confluence, JIRA or Crowd filesystem backup - creates tar.gz of the Installation and Home directories
```

Usage: atlassian_fs_backup [ -c | -j | -w ]
-c --> Backup Confluence filesystem
-j --> Backup JIRA filesystem
-w --> Backup Crowd filesystem
```
* atlassian_full_backup : Performs a complete Confluence, JIRA or Crowd backup (both db and filesystem) - this can be run in a cron job or on-demand
```

Usage: atlassian_full_backup [ -c | -j | -w ]
-c --> Backup Confluence
-j --> Backup JIRA
-w --> Backup Crowd
```
* atlassian_restore_fs_db : Performs a Confluence, JIRA or Crowd restoration taking the database and filesystem back-ups as input
```

Usage: atlassian_restore_fs_db [ -c | -j | -w  ] -s [PATH-TO-SQLDUMP-FILE] -i [PATH-TO-INSTALLDIR-TAR] -h [PATH-TO-HOMEDIR-TAR]
-c        --> Restore a Confluence server
-j        --> Restore a JIRA server
-w        --> Restore a Crowd server
-s PATH-TO-SQLDUMP-FILE   --> Location of the SQL DUMP file
-i PATH-TO-INSTALLDIR-TAR --> Location of the Installation directory archive
-h PATH-TO-HOMEDIR-TAR    --> Location of the Home directory archive
```
* atlassian_rotate_tomcat_logs : Handles the expiration of Tomcat's log files since Atlassian doesn't do this - this should be run as a cron job
```

Usage: atlassian_rotate_tomcat_logs [ -c | -j | -w ]
-c --> Rotate Confluence
-j --> Rotate JIRA
-w --> Rotate Crowd

Example:
0 0 * * * /usr/local/bin/atlassian_rotate_tomcat_logs -c > /usr/local/atlassian/confluence/logs/atlassian_rotate_tomcat_logs.log  2>&1
```
