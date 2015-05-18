#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import MySQLdb
import logging
import logging.config
import simplejson
import argparse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import random
import datetime
import time
import codecs
import pdb
import os

def setup_logging(
    default_path = 'logging.json',
    default_level = logging.INFO,
):
    """Setup logging configuration
    """
    path = default_path

    if os.path.exists(path):
        with open(path, 'r') as f:
            
            config = simplejson.load(f)
            #print f.read()
            logging.config.dictConfig(config)

    else:
        logging.basicConfig(level=default_level)

def db_connection():
    """config mysqldb connection"""
    
    db = MySQLdb.connect(host="127.0.0.1", # your host, usually localhost
        user="mediaWatch", # your username
        passwd="Morefruit2013", # your password
        db="mediaWatch",
        use_unicode=True,
        charset="utf8") # name of the data base
    return db

def get_stat(start):

    # open a driver without GUI on Firefox or Chrome
    # option 1. --- have the browser opened in the remote server
    # option 2. --- running on a Unix/Linux Server. 
    display = Display(visible=0,size=(1024,768))
    display.start()
    driver = webdriver.Firefox()
    
    # br.open("https://news.google.com/")
    driver.get("http://news.google.com")
    # create a cursor
    db = db_connection()
    cur = db.cursor()

    """Fetch all the university KID, name and URL from db"""
    #query = "SELECT KeywordID, Keyword FROM Keywords WHERE category = 'university'"
    query = "SELECT universityformattedname.K_ID,universityformattedname.UniversityName,university_generalinfo.Website FROM newschema.universityformattedname,university_generalinfo where university_generalinfo.K_ID = universityformattedname.K_ID;"
    cur.execute(query)
    university_ID_list = cur.fetchall()

    # for each school, search in its site and get its search result, then
    # update the database
    for i in range(int(start), len(university_ID_list)):
         
        school_url = university_ID_list[i][2]
        school_name = university_ID_list[i][1]
        KeywordID = university_ID_list[i][0]

        logger.critical('---------Working on school: %s--------', i)
        # print general info
        logger.info("Keyword ID: %s", KeywordID)
        logger.info("School Name: %s",school_name)
        logger.info("School Url: %s", school_url)
        
        # 1. searching for news index of university name
        
        try:
            # open "news.google.com" in the browser
            driver.get("http://news.google.com")
            #find input window
            time.sleep(10)
            elem = driver.find_element_by_name("q")
            # clear the search box before sending the key
            elem.clear()
            elem.send_keys(school_name)
            
            
            #click the search button
            search = driver.find_element_by_id("gbqfb")
            search.click()
        
            try:
                time.sleep(20)
                #WebDriverWait(driver,80).until(EC.title_contains(school_name))
                exposure = driver.find_element_by_id("resultStats").text
                exp_idx = exposure.find("result")
                #print "index = ", exp_idx
                news_index = exposure[6:exp_idx]
                news_index = news_index.replace(',','')
                logger.info("News_Index_num: %s",news_index)
                #logger.info("Google_Reference_num: %s", google_reference)
            except:
                logger.error('Search result time out')

            #2. searching for google reference of university name
                
            #open "www.google.com" in the browser
            driver.get("http://www.google.com")
            #find input window
            time.sleep(10)
            elem = driver.find_element_by_name("q")
            # clear the search box before sending the key
            elem.clear()
            elem.send_keys(school_name)
                        
            #click the search button
            search = driver.find_element_by_id("gbqfb")
            search.click()

            try:
                time.sleep(20)
                #WebDriverWait(driver,80).until(EC.title_contains(school_name))
                exposure = driver.find_element_by_id("resultStats").text
                exp_idx = exposure.find("result")
                #print "index = ", exp_idx
                google_reference = exposure[6:exp_idx]
                google_reference = google_reference.replace(',', '')
                logger.info("Google_Reference_num: %s", google_reference)
            except:
                logger.error('Search result time out')

            # 3. searching for google index of university url
            
            #find input window
            time.sleep(10)
            elem = driver.find_element_by_name("q")
            # clear the search box before sending the key
            elem.clear()
            elem.send_keys("site:"+school_url)
            
            #click the search button
            search = driver.find_element_by_id("gbqfb")
            search.click()

            try:
                time.sleep(20)
                #WebDriverWait(driver,80).until(EC.title_contains(school_name))
                exposure = driver.find_element_by_id("resultStats").text
                exp_idx = exposure.find("result")
                #print "index = ", exp_idx
                google_index = exposure[6:exp_idx]
                google_index = google_index.replace(',', '')
                logger.info("Google_Index_num: %s", google_index)

                #insert into database
                query = "INSERT INTO Google_Index VALUES(default,%s,default,%s,%s,%s)"
                cur.execute(query, (KeywordID, news_index,google_index,google_reference))
                logger.info("Inserted into db")
                db.commit()
                time.sleep(20)
            except:
                logger.error('Search result time out')
    
        except:
            logger.error('Google time out')
            
        logger.critical('---------Finished school: %s--------', i)
    driver.quit()
    db.close()
    
    
    
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("last_university_index")
    args = parser.parse_args()

    # create a file handler
    handler = logging.FileHandler('univeristy_output.log')

    # create formatter
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)

    # create(get) the logger object
    logger = logging.getLogger('university_output')
    setup_logging(default_path = 'logging.json', default_level = logging.INFO,
    )

    # add the handlers to the logger
    logger.addHandler(handler)

    # run the cralwer 
    get_stat(args.last_university_index)

