#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import os.path
import sys
import time
from fnmatch import fnmatch

if os.geteuid() != 0:
    print("You must be root to execute this script.")
    sys.exit(1)

parser = ArgumentParser(description="Manage the expiration of Atlassian Tomcat log files.")
parser.add_argument('-c', '--confluence', action='store_true', help="Rotate Confluence Tomcat logs.")
parser.add_argument('-j', '--jira', action='store_true', help="Rotate JIRA Tomcat logs.")
args = parser.parse_args()

install_dir = "/usr/local/atlassian"
num_days = 180
current_time = time.time()
save_time = current_time - (num_days * 86400)

if args.confluence:
    tomcat_log_dir = f"{install_dir}/confluence/logs"
elif args.jira:
    tomcat_log_dir = f"{install_dir}/jira/logs"
else:
    parser.error('Please specify -c or -j for log rotation.')

if not os.path.exists(tomcat_log_dir):
    print(f"Tomcat log directory {tomcat_log_dir} could not be accessed.")
    sys.exit(1)

for rootdir, dirs, files in os.walk(tomcat_log_dir):
    for file in files:
        file_path = os.path.join(rootdir, file)
        file_stat = os.stat(file_path)

        if fnmatch(file_path, '*.????-??-??*'):
            # If file's modificaiton time is earlier than save_time
            # This means the file hasn't been touched in at least num_days
            # Therefore remove it
            if file_stat.st_mtime <= save_time:
                try:
                    os.remove(file_path)
                except:
                    print(f"Unable to remove {file_path}.")
