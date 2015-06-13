#!/usr/bin/python

'''
Created on May 17, 2015

@author: lu
'''

import sys
import os
os.chdir("/home/dev/crawling_lu/auto_processing")

from crawl_bd_gg import crawl_search_counts
from calculate_index import calculate_indexes
from import_db import import_to_db

f_schools = 'school_info.csv'
f_counts = crawl_search_counts(f_schools)
f_indexes, f_composite_indexes = calculate_indexes(f_counts)
#f_indexes = 'indexes_2015_06_04_09_00_03'
#f_composite_indexes = 'composite_index_2015_06_04_09_00_03'
date = '-'.join(f_indexes.split('_')[1:4])
print '++++++++++' + date + '+++++++++++'
print ''
print 'index files: ' + f_indexes, f_composite_indexes
print ''

try:
    import_to_db('184.72.247.127', f_composite_indexes, f_indexes, date) # glogou_production_server
    print date, '184.72.247.127 task successful'
except Exception:
    print sys.exc_info(), '184.72.247.127 failed'
print ''

try:
    import_to_db('localhost', f_composite_indexes, f_indexes, date) # glogou_production_server
    #import_to_db('54.235.87.95', f_composite_indexes, f_indexes, date) # glogou_crawling_sever
    print date, 'localhost 54.235.87.95 task successful'
except Exception:
    print sys.exc_info(), 'localhost 54.235.87.95 failed'
print ''

try:
    import_to_db('107.21.205.192', f_composite_indexes, f_indexes, date) # glogou_backup_server
    print date, '107.21.205.192 task successful'
except Exception:
    print sys.exc_info(), '107.21.205.192 failed'
print ''

print '++++++++++' + date + '+++++++++++'
