import MySQLdb
from _ast import List

conn = MySQLdb.connect(host = 'localhost', 
                       user = 'mediaWatch', 
                       passwd = 'Morefruit2013', 
                       db = 'mediaWatch_lu',
                       charset='utf8', # some school names has unicode
                       use_unicode=True)
x = conn.cursor()

# 'baidu_index_ch','baidu_index_en', 'baidu_news_ch', 'baidu_news_en', 
#              'baidu_site', 'google_index_en', 'google_index_hk', 'google_news', 
#              'google_site', 'yahoojap_index_en', 'yahoojap_index_jp'

def import_google_index_en(list_index, date):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into google_index_en values (%s, %s, %s)"
                  % (entry[0], entry[1], date))
        
def import_google_index_hk(list_index, date):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into google_index_hk values (%s, %s, %s)"
                  % (entry[0], entry[1], date))
        
def import_google_news(list_index, date):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into google_news values (%s, %s, %s)"
                  % (entry[0], entry[1], date))
        
def import_google_site(list_index, date):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into google_site values (%s, %s, %s)"
                  % (entry[0], entry[1], date))
        
def import_baidu_index_ch(list_index, date):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into baidu_index_ch values (%s, %s, %s)"
                  % (entry[0], entry[1], date))

def import_baidu_index_en(list_index, date):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into baidu_index_en values (%s, %s, %s)"
                  % (entry[0], entry[1], date))

def import_baidu_news_ch(list_index, date):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into baidu_news_ch values (%s, %s, %s)"
                  % (entry[0], entry[1], date))

def import_baidu_news_en(list_index, date):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into baidu_news_en values (%s, %s, %s)"
                  % (entry[0], entry[1], date))

def import_baidu_site(list_index, date):
    # list_index is a list of [id, index] entries
    for entry in list_index:
        x.execute("insert into baidu_site values (%s, %s, %s)"
                  % (entry[0], entry[1], date))

if __name__ == '__main__':
    with open('index_arr', 'r') as f_input:
        # input file has 10 cols including id and 9 indexes
        list_index = [] # 9 lists of [id, index] entries
        for i in range(9):
            list_index.append([])
        for line in f_input.readlines():
            index_for_school = line.strip().split('\t')
            for i in range(9):
                list_index[i].append([index_for_school[0], index_for_school[i + 1]])
        date = raw_input('Enter the date (eg, 2015-04-08): ')
        
        import_google_index_en(list_index[0], date)
        import_google_index_hk(list_index[1], date)
        import_google_news(list_index[2], date)
        import_google_site(list_index[3], date)
        import_baidu_index_ch(list_index[4], date)
        import_baidu_index_en(list_index[5], date)
        import_baidu_news_ch(list_index[6], date)
        import_baidu_news_en(list_index[7], date)
        import_baidu_site(list_index[8], date)
        
        do_import = raw_input('Do you want to commit import to database? y/n: ')
        if do_import.lower() == 'y':
            conn.commit()
            print 'Data import successful'
        else:
            print 'Abort import'
        