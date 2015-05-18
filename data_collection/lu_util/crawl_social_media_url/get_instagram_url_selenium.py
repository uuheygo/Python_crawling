from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import MySQLdb
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from time import sleep
import random
import math

def get_linkedin_url_selenium(file_name):
    browser = webdriver.Firefox()
    #browser = webdriver.Chrome(executable_path='/home/lu/Documents/chromedriver')
    f_error = open('errors_' + str(int(random.random() * 10000)), 'w')
    f_success = open('success_' + str(int(random.random() * 10000)), 'w')
    
    all_schools = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            all_schools.append(line)
    print all_schools
    
    count = 0
    for school in all_schools[0:]:
        count += 1
        sleep(random.random() * 1 + 3)
        try:
            # google
            # get the the search result page
            browser.get('https://www.google.com/')
            search_box = browser.find_element_by_id('lst-ib')
            #print search_box
            search_box.send_keys('site:instagram.com ' + school[1] + '\n')
            WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "rso")));
            links = browser.find_element_by_id('rso').find_elements_by_tag_name('a')
            for link in links:
                href = link.get_attribute('href')
                if 'instagram.com' in href and 'https' in href and len(href) < 100:
                    f_success.write(school[0] + '\t' + href + '\n')
                    f_success.flush()
                    break
            else: 
                f_error.write(school[0] + '\t' + school[1] + '\n')
                print school[0] + '\t' + school[1]
                f_error.flush()
            
            # bing
#             browser.get('https://www.bing.com/')
#             search_box = browser.find_element_by_id('sb_form_q')
#             #print search_box
#             search_box.send_keys(school[1] + ' instagram.com\n')
#             WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "b_results")));
#             blocks = browser.find_element_by_id('b_results').find_elements_by_class_name('b_algo')
#             links = []
#             for block in blocks:
#                 links += block.find_elements_by_tag_name('a')
#             #print links
#             for link in links:
#                 href = link.get_attribute('href')
#                 if 'youtube.com' in href and 'user' in href and len(href) < 100:
#                     f_success.write(school[0] + '\t' + href + '\n')
#                     f_success.flush()
#                     break
#             else: 
#                 f_error.write(school[0] + '\t' + school[1] + '\n')
#                 print school[0] + '\t' + school[1]
#                 f_error.flush()
        except Exception:
            f_error.write(school[0] + '\t' + school[1] + '\n')
            print school[0] + '\t' + school[1]
            f_error.flush()
            pass
    f_error.close()
    f_success.close()
    
if __name__ == '__main__':
    get_linkedin_url_selenium('errors_9489')