#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import os.path
import shutil
import sys
import pwd
import subprocess
import tarfile
import re

if os.geteuid() != 0:
    print("You must be root to execute this script.")
    sys.exit(1)

parser = ArgumentParser(description="Automates the procedure for restoring Confluence or JIRA filesystem and database backups.")
parser.add_argument('-c', '--confluence', action='store_true', help="Rotate Confluence Tomcat logs.")
parser.add_argument('-j', '--jira', action='store_true', help="Rotate JIRA Tomcat logs.")
parser.add_argument('-s', '--sqldump', required=True, help="Path to the SQL DUMP file.")
parser.add_argument('-i', '--installdir', required=True, help="Path to the installation directory archive.")
parser.add_argument('-d', '--homedir', required=True, help="Path to the home directory archive.")
args = parser.parse_args()

# Common directories between Confluence and JIRA
home_dir = "/var/atlassian/application-data"
install_dir = "/usr/local/atlassian"

if args.confluence:
    app_name = "confluence"
    env_file = f"{install_dir}/confluence/bin/user.sh"
    dbxml_cfg = f"{home_dir}/confluence/confluence.cfg.xml"
    port_num = 8090
elif args.jira:
    app_name = "jira"
    env_file = f"{install_dir}/jira/bin/user.sh"
    dbxml_cfg = f"{home_dir}/jira/dbconfig.xml"
    port_num = 8080
else:
    parser.error('Please specify -c or -j for restoration of files and database.')

# Perform checks to determine if this script can run on this server
# -------------------------------------------------------------------

# Determine if app_name is installed by checking for existense of env_file
if not os.path.exists(env_file):
    print(f"It looks like {app_name} is not installed")
    print(f"Please ensure {app_name} is installed")
    sys.exit(1)

# Determine if a dedicated app_name user account exists
try:
    pwd.getpwnam(app_name)
except:
    print(f"A dedicated {app_name} user account was not found on this system.")
    print(f"Please ensure {app_name} is installed and runs under a {app_name} user account.")
    sys.exit(1)

# Determine if app_name is running
process = subprocess.run(["systemctl", "status", f"{app_name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout_list = process.stdout.decode().split('\n')
# Nested list comprehension first looking for 'Active:' and then looking for '(running)'
proc_status = [word for word in [active_line for active_line in stdout_list if 'Active:' in active_line][0].split() if '(running)' in word][0]
if proc_status == '(running)':
    print(f"{app_name} is running. Ensure {app_name} is stopped before running this script.")
    sys.exit(1)

# Determine if the sqldump, installdir, and homedir archive files exist
for file in [args.sqldump, args.installdir, args.homedir]:
    if not os.path.exists(file):
        print(f"The file {file} does not exist.")
        sys.exit(1)

# -------------------------------------------------------------------
# Checks Complete

# Begin the restoration procedures
# -------------------------------------------------------------------

# If necessary remove the existing app_name installation and home directories
# This ensures a clean environment for the extraction of the tar files
for app_dir in [f"{install_dir}/{app_name}", f"{home_dir}/{app_name}"]:
    if os.path.isdir(app_dir):
        try:
            shutil.rmtree(app_dir)
        except:
            print(f"Unable to remove {app_dir}.")
            sys.exit(1)

# Untar the archive files of the Install and Home directories
for archive_path, unpack_path in {f"{args.installdir}":f"{install_dir}", f"{args.homedir}":f"{home_dir}"}:
    print(f"Unpacking {archive_path} to {unpack_path}")
    try:
        tf = tarfile.open(f"{archive_path}")
        tf.extractall(path=f"{unpack_path}")
        tf.close()
    except:
        print(f"Unable to unpack {archive_path} to {unpack_path}.")
        sys.exit(1)


# Check for existence of root user's .my.cnf file
# which contains the databse connection information
if not os.path.isfile("/root/.my.cnf"):
    print("The path to database connection information does not exist.")
    sys.exit(1)

# Before restoring the database, we will drop all existing tables to ensure a clean start
print(f"Dropping all tables from {dbname} - if this is correct press Enter - otherwise CTRL-C")
s = input()
