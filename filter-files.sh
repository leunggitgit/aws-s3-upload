#
# filter_file.sh
# Author: Steve Leung
#
# Usage:
#    sh filter_file.sh [<source directory>] [<output file>]
#

# TODO: update DEFAULT_DIR
DEFAULT_DIR=/usr/lib
DEFAULT_OUTFILE=tmp-filter-files.out

if [ "$1" = "" ]; then
    SOURCE_DIR=$DEFAULT_DIR
else
    SOURCE_DIR="$1"
fi

if [ "$2" = "" ]; then
    OUTFILE=$DEFAULT_OUTFILE
else
    OUTFILE="$2"
fi

find $SOURCE_DIR -type f > $OUTFILE

