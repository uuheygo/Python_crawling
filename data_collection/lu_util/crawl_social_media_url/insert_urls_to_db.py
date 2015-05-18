import MySQLdb

conn = MySQLdb.connect(host = 'localhost', 
                       user = 'mediaWatch', 
                       passwd = 'Morefruit2013', 
                       db = 'mediaWatch_lu',
                       charset='utf8', # some school names has unicode
                       use_unicode=True)
x = conn.cursor()

def insert_url(filename):
    with open(filename, 'r') as f:
        for line in f.readlines():
            id, url = line.strip().split()
            #print id, url
            x.execute('''update school set youtube_url="%s" where id=%s''' % (url, id,))
        conn.commit()
            
if __name__ == '__main__':
    insert_url('youtube_url.txt')