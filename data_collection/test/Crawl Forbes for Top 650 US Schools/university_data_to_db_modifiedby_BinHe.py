#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import MySQLdb
import logging
import logging.config
import simplejson
import argparse
from bs4 import BeautifulSoup

import mechanize
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
import random
import datetime
import time
import codecs
import pdb
import os
import sys

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


def connect_to_DB():
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
		user="mediaWatch", # your username
		passwd="Morefruit2013", # your password
		db="mediaWatch",
		use_unicode=True,
		charset="utf8") # name of the data base
    return db

def read_DB():
    ''' read general school info from database table overall_school_list '''
    db = connect_to_DB()
    cur = db.cursor()
    sql = 'SELECT Over.Rank, K.KeywordID FROM mediaWatch.overall_school_list as Over left join Keywords as K on Over.Name = K.Keyword order by Over.Rank'
    try:
        cur.execute(sql)
        overall_list = cur.fetchall()
        db.close()
        return overall_list

    except MySQLdb.Error, e:
        print e
        return -1


def info_init():
    info = {
	'Rank': u'999',
	'Name': 'N/A',
	'State': 'N/A',
	'Tel': 'N/A',
	'Website':'N/A',
	'Student_Population': None,
	'Undergraduate_Population': None,
	'Student_to_Faculty_Ratio': 'N/A',
	'Total_Annual_Cost': None,
	'In_State_Tuition': None,
	'Out_of_State_Tuition': None,
	'Percent_on_Financial_Aid':None,
	'Percent_Admitted':None,
	'SAT_Composite_Range':'N/A',
	'Forbes_Financial_Grade':'N/A',
	'Private_Colleges':None,
	'Research_Universities': None,
	'the_Northeast': None,
	'the_Midwest':None,
	'the_South': None,
	'the_West': None,
	'Male': None,
	'Female':None,	
	'American_Indian_or_Alaskan_native':None,
	'Asian_Native_Hawaiian_Pacific_Islander': None,
	'Black_or_African_American': None,
	'Hispanic_Latino':None,
	'White': None,
	'Two_or_More_Races': None,
	'Race_Ethnicity_Unknown': None,
	'Non_Resident_Alien': None,
	'Full_Time': None,
	'Part_Time': None,
	'Year': u'2014',
	'Funding': 0,
    'ACT_Composite_Range': 'N/A',
    }
    return info
    
def start(file_name):
    #overall_list = read_DB()
    db = connect_to_DB()
    cur = db.cursor()
    
#    for each_school in schools:
#	fund_db = #insert into university_fundraising () values
#	generalinfo_db = #insert into university_generalinfo () values
#	population_db = #insert into university_population () values 
#	rank_db = #insert into university_ranking () values
    col1 = 'Rank'
    col2 = 'Name'
    col3 = 'State'
    col4 = 'Tel'
    col5 = 'Website'
    col6 = 'Student_Population'
    col7 = 'Undergraduate_Population'
    col8 = 'Student_to_Faculty_Ratio'
    col9 = 'Total_Annual_Cost'
    col10 = 'In_State_Tuition'
    col11 = 'Out_of_State_Tuition'
    col12 = 'Percent_on_Financial_Aid'
    col13 = 'Percent_Admitted'
    col14 = 'SAT_Composite_Range'
    col15 = 'Forbes_Financial_Grade'
    col16 = 'Private_Colleges'
    col17 = 'Research_Universities'
    col18 = 'the_Northeast'
    col19 = 'the_Midwest'
    col20 ='the_South'
    col21 = 'the_West'
    col22 = 'Male'
    col23 = 'Female'	
    col24 = 'American_Indian_or_Alaskan_native'
    col25 = 'Asian_Native_Hawaiian_Pacific_Islander'
    col26 = 'Black_or_African_American'
    col27 = 'Hispanic_Latino'
    col28 = 'White'
    col29 = 'Two_or_More_Races'
    col30 = 'Race_Ethnicity_Unknown'
    col31 = 'Non_Resident_Alien'
    col32 = 'Full_Time'
    col33 = 'Part_Time'
    col34 = 'Year'
    col35 = 'Funding'
    col36 = 'ACT_Composite_Range'
    
    school_info = info_init()
    #max_len = 0
    #rank_num = 0
    with codecs.open(file_name, 'r', 'utf-8') as reader:
	count = 0
        for i, school_name in enumerate(reader):
            content = school_name.replace("\r","").replace("\n","").strip()
            logger.info("content=%s", content)
            if content == "############### Next ###############":
               #pre-setup, convert each column into predefined data type
                if school_info[col12]:
                    school_info[col12] = float(school_info[col12].replace("%",""))/100
                if school_info[col13]:
                    school_info[col13] = float(school_info[col13].replace("%",""))/100
                if school_info[col22]:
                    school_info[col22] = float(school_info[col22].replace("%",""))/100
                if school_info[col23]:
                    school_info[col23] = float(school_info[col23].replace("%",""))/100
                if school_info[col24]:
                    school_info[col24] = float(school_info[col24].replace("%",""))/100
                if school_info[col25]:
                    school_info[col25] = float(school_info[col25].replace("%",""))/100
                if school_info[col26]:
                    school_info[col26] = float(school_info[col26].replace("%",""))/100
                if school_info[col27]:
                    school_info[col27] = float(school_info[col27].replace("%",""))/100
                if school_info[col28]:
                    school_info[col28] = float(school_info[col28].replace("%",""))/100
                if school_info[col29]:
                    school_info[col29] = float(school_info[col29].replace("%",""))/100
                if school_info[col30]:
                    school_info[col30] = float(school_info[col30].replace("%",""))/100
                if school_info[col31]:
                    school_info[col31] = float(school_info[col31].replace("%",""))/100
                if school_info[col32]:
                    school_info[col32] = float(school_info[col32].replace("%",""))/100
                if school_info[col33]:
                    school_info[col33] = float(school_info[col33].replace("%",""))/100

                if school_info[col6]:
                    school_info[col6] = int(school_info[col6].replace(",",""))
                if school_info[col7]:
                    school_info[col7] = int(school_info[col7].replace(",",""))
                if school_info[col9]:
                    school_info[col9] = int(school_info[col9].replace("$","").replace(",",""))
                if school_info[col10]:
                    school_info[col10] = int(school_info[col10].replace("$","").replace(",",""))
                if school_info[col11]:
                    school_info[col11] = int(school_info[col11].replace("$","").replace(",",""))

                #mysql insert statement for each table
                condition_clause = "select KeywordID from Keywords where category='University' and Keyword = %s"
                cur.execute(condition_clause, school_info['Name'])
                k_id = cur.fetchone()[0]
                logger.info("k_id = %s", k_id)

                query_generalinfo="insert into university_temp values (default, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                #query_generalinfo="update university_temp set ACT_Composite_Range = %s where K_ID = %s"

                try:
                    cur.execute(query_generalinfo, (k_id, school_info[col1], school_info[col2], school_info[col3], school_info[col4], school_info[col5], school_info[col6], school_info[col7], school_info[col8], school_info[col9], school_info[col10], \
                                                    school_info[col11], school_info[col12], school_info[col13], school_info[col14], school_info[col15], school_info[col16], school_info[col17], school_info[col18], school_info[col19], school_info[col20], \
                                                    school_info[col21], school_info[col22], school_info[col23], school_info[col24], school_info[col25], school_info[col26], school_info[col27], school_info[col28], school_info[col29], school_info[col30], \
                                                    school_info[col31], school_info[col32], school_info[col33], school_info[col34], school_info[col35], school_info[col36]))
                    logger.info("generalinfo: %s", query_generalinfo)
                    #cur.execute (query_generalinfo, (school_info[col36],k_id))
                except Exception as e:
                    logger.error("critical generalinfo: %s", e)
                    pass

                count = count+1
                school_info = info_init()

            elif content[0]=='#':
                parts  = content.split(' in ')
                value = parts[0][1:]
                key = parts[1].strip().replace(" ","_")
                school_info[key] = value
                #logger.info("key = %s", key)
                #logger.info("value = %s", value)
            else:
                detail = content.split(":")
                if (len(detail) == 2):
                    key = detail[0].strip().replace("\r","").replace("\n","").replace(" ","_").replace("/","_").replace("-","_")
                    value = detail[1].strip().replace("\r","").replace("\n","")
                    school_info[key] = value
                    #logger.info("key = %s", key)
                    #logger.info("value = %s", value)
                elif (len(detail) > 2 ):
                    key = detail[0].strip().replace("\r","").replace("\n","").replace(" ","_").replace("/","_").replace("-","_")
                    index = content.find(":")
                    value = content[index+1:].strip()
                    school_info[key] = value
                    #logger.info("key = %s", key)
                    #logger.info("value = %s", value)
                else:
                    logger.error("detail has less than 2 colons and not start with #, detail= %s", detail)
                    logger.error("school_info: %s", school_info)
                    #pdb.set_trace()

            #pdb.set_trace()
        db.commit()
        db.close()
        logger.info('count = %s', count)
    
if __name__ == '__main__':
    logger = logging.getLogger('dump_to_db')   
    setup_logging(default_path = 'db-logging.json', default_level = logging.INFO,)

    #file_name = sys.argv[1]
    file_name = 'university_detail_1_to_100.txt'
    start(file_name)

