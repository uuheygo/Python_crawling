'''
Created on May 17, 2015

@author: lu
'''
from crawl_bd_gg import crawl_search_counts
from calculate_index import calculate_indexes
from import_db import import_to_db

if __name__ == '__main__':
    f_schools = 'school_info.csv'
    f_counts = crawl_search_counts(f_schools)
    f_indexes, f_composite_indexes = calculate_indexes(f_counts)
    #f_indexes = 'indexes_2015_05_17_10_42_24'
    date = '-'.join(f_indexes.split('_')[1:4])
    import_to_db(f_composite_indexes, f_indexes, date) # need set db connect in import_db module