#
# Usage:
#    python upload.sh [<bucket name>] < <input file containing a list of files>
#
# Author: Steve Leung
#
# Supported directives:
#    #!bucket=<bucket name>
#    #!remove-target-prefix=<prefix to remove>
#    #!set-target-prefix=<prefix to add>
#    #!exit
#
# Assertions:
#    file path does not contain character "=".
#

import sys
import re
import traceback
import time
import boto3

# This specifies the S3 bucket name.
DIR_BUCKET='#!bucket='
# This removes the specified prefix from the target path.
DIR_REMOVE_PREFIX='#!remove-target-prefix='
# This adds the specified prefix to the target path.
DIR_SET_PREFIX='#!set-target-prefix='
# This exits the tool.
DIR_EXIT='#!exit'

bucket=None
remove_prefix=None
set_prefix=None

lines = sys.stdin.readlines()
# total number of lines read
line_read_count = 0
# total number of lines with leading # read
skipped_lines = 0
# total number of lines causing exceptions
error_count = 0
# total number of files successfully uploaded
upload_count = 0

s3 = boto3.resource('s3')

if len(sys.argv) == 2:
    bucket = sys.argv[1]

total_start= time.time()

for line in lines:
    line_read_count += 1

    line= line.strip()
    if len(line) == 0 or line[0] == '#':
        #skip empty line or comment/directive
        skipped_lines += 1

        if line.find(DIR_BUCKET, 0) == 0:
            bucket=line[len(DIR_BUCKET):].strip()
            print('INFO: bucket={}'.format(bucket))
        elif line.find(DIR_REMOVE_PREFIX, 0) == 0:
            remove_prefix=line[len(DIR_REMOVE_PREFIX):].strip()
            print('INFO: remove_prefix={}'.format(remove_prefix))
        elif line.find(DIR_SET_PREFIX, 0) == 0:
            set_prefix=line[len(DIR_SET_PREFIX):].strip()
            print('INFO: set_prefix={}'.format(set_prefix))
        elif line.find(DIR_EXIT, 0) == 0:
            print('INFO: Exiting now because of the presence of exit directive.')
            break

        continue

    #m = re.search('(.+)\s+(.+)', line)
    #m = re.search('(.+)\s*=\s*(.+)', line)

    # pettern matching is greedy.
    m = re.search('(.+)=(.+)', line)
    if m is None:
        two_columns=False
        sfile = line
        tfile = line
        print('INFO: read line file={}'.format(line))
    else:
        two_columns=True
        sfile = m.group(1).strip()
        tfile = m.group(2).strip()
        print('INFO: read line sfile={} tfile={}'.format(sfile, tfile))

    if remove_prefix is not None:
        if tfile.find(remove_prefix) == 0 :    
            tfile = tfile.replace(remove_prefix, '',  1)

    if set_prefix is not None:
        tfile = set_prefix + tfile

    print("INFO: Number of lines read= {}".format(line_read_count))

    if bucket is None:
       print("ERROR: bucket name is not set. Exit now.")
       #sys.exit()
       error_count += 1
       break

    start = time.time()
    try:
        print('INFO: upload_file(sfile={}, tfile={})'.format(sfile, tfile))
        s3.Bucket(bucket).upload_file(sfile, tfile)
        end = time.time()
        upload_count += 1
    except:
        print("ERROR: Get exception while processing sfile={} and tfile={}".format(sfile, tfile))
        print(traceback.format_exc())
        end = time.time()
        error_count += 1
        
    print('INFO: elapsed for uploading one file={} seconds'.format(end - start))

print()
print('############################################################')
print()

print ('line_read_count={}'.format(line_read_count))
print ('skipped_lines={}'.format(skipped_lines))
print ('error_count={}'.format(error_count))
print ('upload_count={}'.format(upload_count))

total_end= time.time()
print('total elapsed={} seconds'.format(total_end - total_start))

