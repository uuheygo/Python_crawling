# -*- encoding: utf-8 -*-
import time, datetime
import MySQLdb
import random
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import urllib, os, pprint
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import requests

def searchUrls(driver, keyword):
    
    driver.get("http://www.google.com")
    
    elem = driver.find_element_by_name("q")
    #elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q"))
    elem.send_keys(keyword)
    elem.send_keys(Keys.RETURN)
    
    time.sleep(random.randint(7, 21))
    
    encoding = 'utf-8'
    find = 0
    page = 1

    time.sleep(random.randint(10,21))
    #WebDriverWait(driver,10).until(EC.title_contains(keyword))
    #print 'googel search url = ', driver.current_url
    web_url = ''
    try:
        ol = driver.find_element_by_id('rso')
        lis = ol.find_elements_by_xpath("//li[contains(@class,'g')]")
        #lis = ol.find_element_by_xpath("//li[contains(@class,'g')]")
        #lis = driver.find_elements_by_xpath("//ol[@id='rso']/li")[0]
        #print 'lis length = ', len(lis)
        if (len(lis) > 0):
            i = 0
            for li in lis: 
                try: 

                    #print 'i = ', i
                    title = li.find_elements_by_xpath("//div/h3/a")
                    #print '-----------------------------------------------------------'
                    #print 'title[' + str(i) + '].text = ' + title[i].text
                    
                    
                    urls = li.find_elements_by_xpath("//div/div/div/div/cite")
                    #print 'urls[' + str(i) + '].text = ', urls[i].text
                    #print '-----------------------------------------------------------'
                    web_url = urls[i].text
                    lower_str = web_url.lower()
                    
                    
                    #print '__________________________________________________________'
                    
                    if (('youtube' in lower_str)  or ('net.com' in lower_str)
                        or ('twitter' in lower_str) or ('dict' in lower_str) or ( 'vimeo' in lower_str)
                        or ('foursquare' in lower_str) or ('wiki' in lower_str) or ('crunch' in lower_str)
                        or ('linkedin' in lower_str) or ('week' in lower_str) or ('report' in lower_str)
                        or ('yahoo' in lower_str)  or ('imdb' in lower_str) or ('pdf' in lower_str) 
			            or ('google' in lower_str) or ('daily' in lower_str) or ('journal' in lower_str)
			            or ('biz' in lower_str)):
                        print 'skip youtube, wiki, crunchbase, linkedin, yahoo, businessweek or report related urls'
                        i = i + 1
                        print '**********skip non-correct one**************'
                        continue
                    else:
                        #print '#########################################################'
                        #print 'the univerity\'s website (web_url) is: ', web_url
                        #pdb.set_trace()
                        
                        #print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                        try: 
                            if u'\u203a' in web_url:
                                print 'found › in web_url = true'
                                web_url = web_url.split(u'\u203a')[0]
                                print 'the univerity\'s website (web_url) is: ', web_url
                        except:
                            print "\'›\' string  exception"
                        i = i + 1
                        #print '#########################################################'
                        break
                except:
                    print 'elements not found'
                    break
            # found in next page
        else:
            print 'no luck in found the website'    
    except:
        print 'No result found in Google search.'

    return driver, web_url
    
def get_facebook_website():

        db = connect_to_database()
        cur= db.cursor()
        #output_file = 'university_url_table.txt'
        #writer = codecs.open(output_file, 'w', encoding='utf-8')
        sql = 'select K_ID, FormattedName from university_basics where Facebook_website is NULL '
        cur.execute(sql)
        schools = cur.fetchall()
        for School in schools:
                k_id = School[0]
                university_name = School[1]
                if (university_name == ""):
                    pass
                else:
                    print 'university name = ', university_name
                    search_string = (university_name+" facebook")
                    try:
                        ############################################
                        # Use Firefox as a search browser
                        ############################################
                        driver = webdriver.Firefox() # Unmark this line to use Firefox

                        ############################################
                        # Use Chrome as a search browser
                        ############################################
                        # Download chromedriver, set up path for your own directory
                        #chromedriver = "/home/chaos/Workbench/Python/glogou/chromedriver"
                        # Import os to setup environment
                        #os.environ["webdriver.chrome.driver"] = chromedriver
                        #driver = webdriver.Chrome(chromedriver)


                        driver.implicitly_wait(10)

                        driver, website = searchUrls(driver, search_string)
                        #searchUrls(univerity_name)
                        print 'website = ', website
                        #try:
                        #    website = website.replace("www", "graph")
                        #    r = requests.get(website)
                        #    likes = json.loads(r.text)

                        #    likesno =  str(likes[u'likes'])
                        #    facebookid = str(likes[u'id'])
                        #except:
                        #    facebookid=""
                        #    likesno =  ""

                        #print likesno
                        #print facebookid
                        driver.quit()
                        try:
                            sql = 'update university_basics set Facebook_website = %s where K_ID = %s'
                            cur. execute(sql, (website, k_id))
                            db.commit()
                        except Exception, e:
                            print k_id, e

                    except:
                        print '%s, facebook website not found'%university_name
        db.close()

def get_facebook_id():

        db = connect_to_database()
        cur= db.cursor()
        #output_file = 'university_url_table.txt'
        #writer = codecs.open(output_file, 'w', encoding='utf-8')
        sql = 'select K_ID, Facebook_website from university_basics where Facebook_ID is NULL and Facebook_website is not NULL '
        cur.execute(sql)
        schools = cur.fetchall()
        for School in schools:
                k_id = School[0]
                url = School[1]
                if (url == ""):
                    pass
                else:
                    print 'facebook website = ', url
                    try:
                        website = url.replace("www", "graph")
                        r = requests.get(website, verify=False)
                        response = json.loads(r.text)

                        #likesno =  str(likes[u'likes'])
                        facebook_id = int(response[u'id'])
                        print 'facebook_id = ', facebook_id

                        try:
                            sql = 'update university_basics set Facebook_ID = %s where K_ID = %s'
                            cur. execute(sql, (facebook_id, k_id))
                            db.commit()
                        except Exception, e:
                            print k_id, e
                            continue

                    except:
                        print 'facebook id not found for %s'%k_id
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
    get_facebook_id()
    print 'read and write finished.'

