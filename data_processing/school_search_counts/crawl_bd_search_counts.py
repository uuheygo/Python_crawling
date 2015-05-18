from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import MySQLdb
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from time import sleep
import random
import math
import unicodedata
import re
import sys
import codecs
import datetime
import time

def get_bd_index_all_selenium(file_name):
    browser = webdriver.Firefox()
    #browser = webdriver.Chrome(executable_path='/home/lu/Documents/chromedriver')
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
    f_error = open('errors_' + st, 'w')
    f_success = open('success_' + st, 'w')
    
    all_schools = []
    with codecs.open(file_name, 'r', 'utf-8') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            all_schools.append(line)
    print all_schools
    
    count = 0
    for school in all_schools[0:]:
        count += 1
        sleep(random.random() * 2)
        nums = []
        try:
            # baidu search
            # en
            if len(school) > 3:
                target_en = "\"" + school[1] + "\" " + school[3]+ "\n"
            else:
                target_en = "\"" + school[1] + "\"\n"
            browser.get('https://www.baidu.com/')
            search_box = browser.find_element_by_id('kw')
            #print search_box
            search_box.send_keys(target_en)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "container")));
            elem = browser.find_element_by_class_name('nums')
            all_txt = elem.get_attribute('innerHTML')
            str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
            #print type(str_txt), str_txt
            nums_en_index = re.findall(r'\d+', str_txt)
            nums.append(''.join(nums_en_index))
             
            #f_success.write(school[0] + '\t' + nums + '\n')
            #f_success.flush()
             
            # baidu news
            # en
            #target_en = school[1] + "\n"
            browser.find_element_by_id('s_tab').find_element_by_tag_name('a').click()
            #search_box = browser.find_element_by_id('ww')
            #print search_box
            #search_box.send_keys(target_en)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "header_top_bar")));
            elem = browser.find_element_by_id('header_top_bar')
            all_txt = elem.get_attribute('innerHTML')
            str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
            #print type(str_txt), str_txt
            nums_en_index = re.findall(r'\d+', str_txt)
            nums.append(''.join(nums_en_index))
            
            
            # baidu search
            # ch
            target_ch = "\"" + school[2] + "\"\n"
            #print target_ch
            #print type(target_ch)
            browser.get('https://www.baidu.com/')
            search_box = browser.find_element_by_id('kw')
            #print search_box
            search_box.send_keys(target_ch)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "container")));
            elem = browser.find_element_by_class_name('nums')
            all_txt = elem.get_attribute('innerHTML')
            str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
            #rint type(str_txt), str_txt
            nums_en_index = re.findall(r'\d+', str_txt)
            nums.append(''.join(nums_en_index))
            
            #f_success.write(school[0] + '\t' + nums + '\n')
            #f_success.flush()
            
            # baidu news
            # ch
            #target_ch = school[1] + "\n"
            browser.find_element_by_id('s_tab').find_element_by_tag_name('a').click()
            #search_box = browser.find_element_by_id('ww')
            #print search_box
            #search_box.send_keys(target_ch)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "header_top_bar")));
            elem = browser.find_element_by_id('header_top_bar')
            all_txt = elem.get_attribute('innerHTML')
            str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
            #print type(str_txt), str_txt
            nums_en_index = re.findall(r'\d+', str_txt)
            nums.append(''.join(nums_en_index))
            
            one_line = school[0] + '\t' + '\t'.join(nums) + '\n'
            f_success.write(one_line)
            f_success.flush()
            print one_line
            
        except Exception:
            print sys.exc_info()
            f_error.write(school[0] + '\t' + school[1] + '\n')
            print '\t'.join(school) + '\n'
            f_error.flush()
            pass
    f_error.close()
    f_success.close()
    
if __name__ == '__main__':
    get_bd_index_all_selenium('school_ch_name_v2.csv')