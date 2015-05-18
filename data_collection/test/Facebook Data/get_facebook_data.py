import time, datetime
import MySQLdb
import random
import json

import requests

def get_facebook_data():

        db = connect_to_database()
        cur= db.cursor()
        #output_file = 'university_url_table.txt'
        #writer = codecs.open(output_file, 'w', encoding='utf-8')
        sql = 'select K_ID, Facebook_ID from university_basics where Facebook_ID is not NULL'
        cur.execute(sql)
        schools = cur.fetchall()
        for School in schools:
                k_id = School[0]
                id = School[1]
                if (id == ""):
                    pass
                else:
                    print 'facebook_id = ', id
                    try:
                        api_url = 'https://graph.facebook.com/'+ str(id)
                        r = requests.get(api_url, verify=False)
                        response = json.loads(r.text)
                        likes_no =  int(response[u'likes'])
                        talking_about_count = int(response[u'talking_about_count'])
                        print 'likes_no = ', likes_no
                        print 'talking_about_count =', talking_about_count

                        try:
                            sql = 'insert into Facebook_Data value (default, %s, %s, default, %s)'
                            cur. execute(sql, (k_id, likes_no, talking_about_count))
                            db.commit()
                        except Exception, e:
                            print k_id, e
                            continue

                    except:
                        print 'facebook data not found for k_id: ',k_id
                        continue
        db.close()

def connect_to_database():

    db = MySQLdb.connect(host="127.0.0.1", \
                         user="mediaWatch", \
                         passwd="Morefruit2013", \
    		             db="mediaWatch", \
                         use_unicode=True, \
                         charset="utf8")
    return db
if __name__ == "__main__":

    #result = get_facebook_website()
    get_facebook_data()