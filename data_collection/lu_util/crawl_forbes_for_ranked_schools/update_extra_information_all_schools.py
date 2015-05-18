from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import MySQLdb
from selenium.webdriver.support.expected_conditions import presence_of_element_located


count_new = 0
browser = webdriver.Firefox()
# create connection to 'mediawatch_lu'
conn = MySQLdb.connect(host = 'localhost', 
                       user = 'mediawatch', 
                       passwd = 'Morefruit2013', 
                       db = 'mediawatch_lu',
                       charset='utf8', # some school names has unicode
                       use_unicode=True)
x = conn.cursor()

def update_extra_infor_all_school():
    x.execute('select forbes_url from school_list')
    school_stored = [elem[0] for elem in x.fetchall()]
    print school_stored
    for school_forbes_url in school_stored:
        update_extra_infor(school_forbes_url)
    
    conn.commit()
    browser.close()
    
def update_extra_infor(school_forbes_url):
    browser.get(school_forbes_url)
    
    if 'welcome' in browser.title: # welcome page appears
         continue_link = WebDriverWait(browser,30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'continue')))
         continue_link.click()
         
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "collegesTop")))
    collegesTop = browser.find_element_by_id('collegesTop')
    school_logo_url = collegesTop.find_element_by_tag_name('img').get_attribute('src')
    addr_infor = collegesTop.find_element_by_class_name('address') \
                            .find_elements_by_tag_name('li')
    
    school_city = None
    school_state_short = None
    try:
        school_city, school_state_short = [elem.strip() for elem in addr_infor[0].text.split(',')]
    except:
        school_state_short = addr_infor[0].text.strip()
        
    school_phone = addr_infor[1].text
    school_url = addr_infor[2].find_element_by_tag_name('a').get_attribute('href')
    
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "bio")))
    try:
        browser.find_element_by_id('moredesc').click() # load full profile by click more
    except:
        pass
    school_profile = browser.find_element_by_id('bio').text
    
    x.execute('select id from school_list where forbes_url=%s', (school_forbes_url))
    school_id = x.fetchall()[0][0]
    x.execute('''
                update school_list 
                set city=%s, state_short=%s, phone=%s, logo_url=%s, url=%s, profile=%s
                where id=%s
             ''', (school_city, school_state_short, school_phone, school_logo_url, school_url, school_profile, school_id))
    print school_id, school_city, school_state_short, school_phone, school_logo_url, school_url
    
    
if __name__ == '__main__':
    update_extra_infor_all_school()
    
    
    
    