# -*- encoding: utf-8 -*-
import os
#from pyvirtualdisplay import Display
import MySQLdb
import mechanize, pprint
from mechanize._html import MechanizeBs
import pprint
import sys
import time, datetime
# regular expression
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import urllib, os, pprint
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import pdb
import random
import codecs
import json
import requests

def db_connection():
    """config mysqldb connection"""
    
    db = MySQLdb.connect(host="127.0.0.1", # your host, usually localhost
        user="root", # your username
        passwd="198926xql", # your password
        db="newschema",
        use_unicode=True,
        charset="utf8") # name of the data base
    return db

def searchName(driver, keyword):
    
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
   
    try:
        ol = driver.find_element_by_id('rso')
        lis = ol.find_elements_by_xpath("//li[contains(@class,'g')]")
        #lis = driver.find_elements_by_xpath("//ol[@id='rso']/li")[0]
        #print 'lis length = ', len(lis)
        if (len(lis) > 0):
            i = 0
            for li in lis: 
                try: 

                    title = li.find_elements_by_xpath("//div/h3/a")
                    #print '-----------------------------------------------------------'
                    #print 'title[' + str(i) + '].text = ' + title[i].text
                    
                    str = title[i].text
                    # print str
                    
                    # get the twitter name after the @ puncutation
                    # Example: Stanford University (@Stanford) | Twitter
                    result = re.search('(?<=@)\w+',str)
                    twitter_name = result.group(0)
                    print "Twitter name: "+twitter_name
                    rso = driver.find_element_by_id('rso')
                    website = rso.find_elements_by_xpath("//cite[contains(@class,'_Rm')]")
                    
                    #//*[@id="rso"]/div[2]/li[1]/div/div/div/div[1]/cite

                    twitter_url = website[i].text    
                    # Open the page "gettwitterid.com" to get key info includes the twitter id, followers of the university     
                    driver.get("http://gettwitterid.com/")
                    elem = driver.find_element_by_name("user_name")
                    
                    elem.send_keys(twitter_name)
                    elem.send_keys(Keys.RETURN)
                    time.sleep(random.randint(7, 21))
                    
                    # find elements in the table
                    table = driver.find_element_by_xpath("//table[contains(@class,'profile_info')]")
                    twitter_id = table.find_element_by_xpath("//tr/td[2]/p")
                    print "hello"
                    print twitter_id
                    uni_name = table.find_element_by_xpath("//tr[2]/td[2]/p")
                    screen_name = table.find_element_by_xpath("//tr[3]/td[2]/p")
                    total_followers = table.find_element_by_xpath("//tr[4]/td[2]/p")
                    total_status = table.find_element_by_xpath("//tr[5]/td[2]/p")
                    print "Twitter ID: " + twitter_id.text
                    print "University Name: " + uni_name.text
                    print "Twitter Url: " + twitter_url
                    print "Screen Name: " + screen_name.text
                    print "Total Followers: " + total_followers.text
                    print "Total Status: " + total_status.text
                    #print table.text
                    
          
                    '''if (('youtube' in lower_str)  or ('net.com' in lower_str)
                        or ('twitter' in lower_str) or ('dict' in lower_str) or ( 'vimeo' in lower_str)
                        or ('foursquare' in lower_str) or ('wiki' in lower_str) or ('crunch' in lower_str)
                        or ('linkedin' in lower_str) or ('week' in lower_str) or ('report' in lower_str)
                        or ('yahoo' in lower_str)  or ('imdb' in lower_str) or ('pdf' in lower_str) 
			or ('google' in lower_str) or ('daily' in lower_str) or ('journal' in lower_str)
			or ('biz' in lower_str) or ('page' in lower_str)):
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
                        break'''
                except:
                    print 'elements not found'
                    break
            # found in next page
        else:
            print 'no luck in found the website'    
    except:
        print 'No result found in Google search.'
                         
    return twitter_id,twitter_url,uni_name,screen_name,total_followers,total_status
    
def get_file(input_file):

        output_file = 'university_url_table6.txt'
        #writer = open (output_file, 'w')
        writer = codecs.open(output_file, 'w', encoding='utf-8')
        print "reader = "+ input_file

        # connect to the db and create a cursor
        db = db_connection()
        cur = db.cursor()
                
        # To run webdriver WITHOUT GUI on Firefox or Chrome, 
        # set up virtual display 
        # install xvfb, xephyr, xvnc, pyvirtualdisplay
        # Ubuntu : sudo apt-get install python-pip
        #        : sudo apt-get install xvfb
        #        : sudo apt-get install xserver-xephyr
        #        : sudo apt-get install tightvncserver
        #        : sudo pip install pyvirtualdisplay
        # import pyvirtualdisplay moduel with Display

        #display = Display(visible = 0, size = (1024, 768))
        #display.start()
        
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
        
        line_no = 0
        with open(input_file, 'r') as reader:
            for university_name in reader:
                
                #print  "pre-processing univerity_name = " + univerity_name
                university_name = university_name.replace("*","").replace("\n","").replace("\r", "").replace("\t", "").strip().decode('utf-8') 
                #print 'univerity name = ', univerity_name
                if (university_name == ""):
                    pass
                else:
                    # get the twitter data from the searchName function
                    twitter_id,twitter_url,uni_name,screen_name,total_followers,total_status = searchName(driver, university_name+" twitter")
                                        
                    print 'write website to output file...'
                    print '============================================================='
                    print ''
                    
                    # write the twitter info of the university into db and the file 
                    twitter_id = twitter_id.text
                    uni_name = uni_name.text
                    screen_name = screen_name.text
                    # the follower and status info get from the web is in the format of "111,222"
                    # get rid of the ',' so as to make string to int type transfer possible  
                    total_followers = total_followers.text
                    total_followers = total_followers.replace(',','')
                    
                    total_status = total_status.text
                    total_status = total_status.replace(',','')

                    # write the twitter info to the file
                    writer.write(str(line_no) + "\t" + university_name + "\t" + twitter_id + "\t" + twitter_url + "\t" + uni_name + "\t" + screen_name + "\t" + total_followers + "\t" + total_status + "\r"+"\n")

                    # find the K_ID of the university
                    university_name = university_name.replace( "'","''")
                    query = "SELECT K_ID FROM mediaWatch.universityformattedname where universityformattedname.UniversityName= '%s' "%university_name
                    cur.execute(query)
                    university_K_ID_list = cur.fetchall()
                    university_K_ID = university_K_ID_list[0][0]
                    # print university_K_ID
                    # print "University K_ID: " + str(university_K_ID)

                    # write the crawled data into the database
                    # DATA TYPE:
                    # K_ID: bigint
                    # Twitter_ID: bigint
                    # Twitter_Website: string
                    # Twitter_followers: bigint
                    # Twitter_Status: bigint
                     
                    query = ""
                    query = "INSERT INTO newschema.twitter_data(Table_ID,K_ID,Twitter_ID,Twitter_website,twitter_followers,Total_Status,Insert_Date) VALUES(default,%d,%d,'%s',%d,%d,default)"
                    
                    cur.execute(query %(university_K_ID, long(twitter_id),twitter_url,long(total_followers),long(total_status)))
                    db.commit()
                    print "Inserted into db"
                    time.sleep(20)

            driver.quit()
            reader.close()
            writer.close()
            print 'totally record '+ str(line_no) +' university into file' 

if __name__ == "__main__":
    #newfile = fileGenerator()
    #result = get_file('test_univerity.txt')
    result = get_file('university_list2.txt')
    print 'read and write finished.'

