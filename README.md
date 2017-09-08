# CSVsonic
CSVsonic - Export Subsonic data to CSV

## Description
This program provides a simple way to export all media library information to a CSV file

## Dependencies
Dependencies include:

- urllib2
- ssl
- json
- unicodecsv
- argparse
- sys

These should be available via pip/easy_install.

## Usage
Usage is pretty easy:

```
python csvsonic.py -h
usage: csvsonic.py [-h] -s SERVER -u USERNAME -p PASSWORD -o OUTFILE

optional arguments:
  -h, --help                          show this help message and exit
  -s SERVER, --server SERVER          SubSonic URL
  -u USERNAME, --username USERNAME    Username
  -p PASSWORD, --password PASSWORD,   Password
  -o OUTFILE, --outfile OUTFILE,      Output File
```

