from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import MySQLdb
from selenium.webdriver.support.expected_conditions import presence_of_element_located

def get_linkedin_url_selenium(file_name):
    browser = webdriver.Firefox()
    f_error = open('errors.txt', 'w')
    
    all_schools = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            all_schools.append(line)
    print all_schools
    
    for school in all_schools:
        try:
            # get the the search result page
            browser.get('https://www.google.com/')
            search_box = browser.find_element_by_id('lst-ib')
            #print search_box
            search_box.send_keys('plus.google.com ' + school[1] + '\n')
            WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "rso")));
            links = browser.find_element_by_id('rso').find_elements_by_tag_name('a')
            for link in links:
                href = link.get_attribute('href')
                if 'plus.google.com' in href:
                    print school[0] + '\t' + href
                    break
            
        except Exception:
            f_error.write(school_name)
            pass
    f_error.close()
    
if __name__ == '__main__':
    get_linkedin_url_selenium('school_name_list.csv')