import MySQLdb
import random

conn = MySQLdb.connect(host = 'localhost', 
                       user = 'mediaWatch', 
                       passwd = 'Morefruit2013', 
                       db = 'mediaWatch_lu',
                       charset='utf8', # some school names has unicode
                       use_unicode=True)
x = conn.cursor()

def populate(table_name, start, end):
    for row_num in range(start, end + 1):
        index = random.random() * 10
        
        x.execute("insert into %s values (%%s, %%s, '2015-04-01')" # 04-01 to 04-23
                  % table_name, (row_num, index,))
    conn.commit()
    
if __name__ == '__main__':
    tables = ['baidu_index_ch','baidu_index_en', 'baidu_news_ch', 'baidu_news_en', 
             'baidu_site', 'google_index_en', 'google_index_hk', 'google_news', 
             'google_site', 'yahoojap_index_en', 'yahoojap_index_jp'] 

    for table in tables:
        populate(table, 1, 650)
    
    
    
    