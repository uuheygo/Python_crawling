'''
Created on Apr 9, 2015

@author: Lu Peng
'''

# What: update the school_list table and create school_infor_XXXX of the year
# When: run once a year when school ranking is updated (use year_ranking.txt to find out if it's a new year)
# How: 1. use selenium to browse through the list of ranked schools (650) at "http://www.forbes.com/top-colleges/list/"
#      2. only add new ranked schools of the year with two steps: 
#         a. use the list to add id (auto-increment), forbes url, name, state(ful); 
#         b. get the difference between old list and new list, and go to individual schools to add school_url, 
#            school_city, school_state_short, school_phone, school_logo_url
#      3. create new school_infor_XXXX of the year (foregin key is id references id in school_list): 
#         a. get the all ids and forbes urls from school_list table
#         b. go to each individual forbes school page and gether and insert the information into the table (3 hrs)
#         c. in case of failure, check update progress in the table and use get_yearly_information_all_school.py
#            to pick up and finish off the rest

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

def crawl_school_list():
    # Set up browser and guided to a waiting page

    url = "http://www.forbes.com/top-colleges/list/"
    browser.get(url)
    print browser.current_url
    
    try:
        # Go to school list page by clicking on "continue to site"
        continue_link = WebDriverWait(browser,30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'continue')))
        continue_link.click()
        assert 'America\'s Top Colleges' in browser.title
        
        # check if this is a new ranking of a new year, otherwise abort
        print '---updating school_list---'
        year = browser.find_element_by_id('thelist').get_attribute('data-year') # find the year of ranking
        
        ####### for test only #######
#         try:
#             x.execute("drop table if exists school_infor_%s" % MySQLdb.escape_string(year))
#             conn.commit()
#             print 'drop existing table'
#         except:
#             pass
#         x.execute('truncate table school_list') # delete all rows and set auto-increment to 0
#         conn.commit()
#         open('year_ranking.txt', 'w').close()
        #############################
        
        file = open('year_ranking.txt','a+') # retrieve year data from year_ranking.txt
        year_exists_msg =  'ranking of ' + year + ' has already be crawled\n---abort---'
        for line in file:
            assert year not in line, year_exists_msg # duplicate information
        file.write('\n' + year + '\n')
        file.close()
        print 'found new ranking of',year
        
        ############################
        # update school_list table #
        ############################
        school_stored = fetch_school_forbes_urls()
        
        # get school information on current page, save to db table school_list, and go to next page
        while True:
            # get all new school name and forbes url and save to school_list table
            save_schools_to_db(school_stored)
            # Go to next page if possible
            next_btn = browser.find_element_by_class_name('next') # Find next button
            assert next_btn
            if('disabled' in next_btn.get_attribute('class')):
                print 'school_list renewed\n'
                break
            next_btn.click()
        # commit db change
        conn.commit()
        
        print '---update address of new schools---'
        # get updated school forbes url list
        updated_school_stored = fetch_school_forbes_urls()
        # get the new schools' url
        new_schools_url = [elem for elem in updated_school_stored if elem not in school_stored]
        # store address information in school_list table
        for school_forbes_url in new_schools_url:
            update_extra_infor(school_forbes_url)
        
        # commit db change
        conn.commit()
        print '---', count_new, 'new schools added to database---\n'
        
        # do it separately
#         ###############################################
#         # create table school_infor_XXXX for new year #
#         ###############################################
#         update_yearly_infor(year)
#         
#         # commit db change
#         conn.commit()
#         print '---table for school information of', year, 'created---\n'
        
    except Exception, err:
        print Exception, err
    finally:
        browser.quit()

# fetch school forbes url in school_list table
def fetch_school_forbes_urls():
    x.execute('select forbes_url from school_list')
    school_stored = [elem[0] for elem in x.fetchall()] # fetchall returns a tuple of tuples, take the first of every tuple
    return school_stored
    
# crawl information on current page without adding schools that are already in the database
def save_schools_to_db(school_stored):
    # get current page number
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "paginate")));
    print '\n', browser.current_url
    page_index = browser.find_element_by_class_name('paginate') \
                    .find_element_by_class_name('active') \
                    .find_element_by_tag_name('a') \
                    .text
    print '---extracting information on page', page_index + '---'
    
    # find the table of schools in page
    table = browser.find_element_by_id('listbody')
    school_rows = table.find_elements_by_tag_name('tr')
    
    # if a new school, update db table school_list
    # create school_infor_XXXX
    global count_new # count total new schools
    for school in school_rows:
        school_forbes_url = school.find_element_by_tag_name('a').get_attribute('href')
        school_name = school.find_element_by_tag_name('h3').text.encode('utf-8') # unicode character \u2014
        school_state_full = (school.find_elements_by_tag_name('td'))[2].text
        
        # compare school_forbes_url(unicode) instead of name due to name collision
        # only store new schools in school_list table
        if unicode(school_forbes_url) not in school_stored: 
            x.execute('''
                insert into school_list (name, forbes_url, state_full) values (%s, %s, %s)
             ''', (school_name, school_forbes_url, school_state_full))
            count_new += 1
            print count_new,' - new school added: ', school_name, school_state_full
                   
# get city, state_short, phone, logo, url, profile from school page
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

# update school yearly information for every school(rank, tuition, student's number, etc. could be different)
def update_yearly_infor(year):
    # create a table to store new yearly information
    
    try:
        x.execute('''create table school_infor_%s if not exists (
                id int not null primary key,
                overall_rank int,
                student_population varchar(10),
                undergrad_population varchar(10),
                student_faculty_ration varchar(10),
                annual_cost varchar(10),
                in_state_tuition varchar(10),
                out_state_tuition varchar(10),
                financial_aid_percentage varchar(10),
                admission_percentage varchar(10),
                sat_range varchar(50),
                act_range varchar(50),
                financial_grade varchar(10),
                enroll_male_percentage varchar(10),
                enroll_female_percentage varchar(10),
                enroll_americanindiannative_percentage varchar(10),
                enroll_asian_pacific_percentage varchar(10),
                enroll_black_percentage varchar(10),
                enroll_latino_percentage varchar(10),
                enroll_white_percentage varchar(10),
                enroll_towormoreraces_percentage varchar(10),
                enroll_raceunknown_percentage varchar(10),
                enroll_nonresidentalien_percentage varchar(10),
                fulltime_percentage varchar(10),
                parttime_percentage varchar(10),
                foreign key(id) references school_list(id)
                )''' % MySQLdb.escape_string(year))
        conn.commit()
        print 'created table school_infor_' + year
    except:
        pass
    
    
    x.execute('select id, forbes_url from school_list')
    schools = [(elem[0], elem[1]) for elem in x.fetchall()]
    for school in schools:
        browser.get(school[1])
        
        if 'welcome' in browser.title: # welcome page appears
            continue_link = WebDriverWait(browser,30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'continue')))
            continue_link.click()
            
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "all")));
        school_id = school[0]
        overall_rank = int(browser.find_element_by_class_name('rankonlist').text.split()[0][1:])
        
        stats = browser.find_element_by_class_name('ataglanz')
        numbers = stats.find_elements_by_tag_name('b')
        iterator_numbers = iter(numbers) # convert list to iterator in case some elements doesn't exist
        
        student_population = next(iterator_numbers).text
        undergrad_population = next(iterator_numbers).text
        student_faculty_ration = next(iterator_numbers).text
        annual_cost = next(iterator_numbers).text
        
        in_state_tuition = None
        out_state_tuition = None
        financial_aid_percentage = None
        if annual_cost.strip()[1] != '0':
            in_state_tuition = next(iterator_numbers).text
            out_state_tuition = next(iterator_numbers).text
            financial_aid_percentage = next(iterator_numbers).text
        
        admission_percentage = None
        if 'Percent Admitted' in stats.text:
            admission_percentage = next(iterator_numbers).text
        
        sat_range = None
        act_range = None
        try:
            sat_range = next(iterator_numbers).text
            act_range = next(iterator_numbers).text
        except:
            pass
        
        financial_grade = None
        try:
            financial_grade = browser.find_element_by_class_name('financial-grade').find_element_by_tag_name('b').text
        except:
            pass
        
        # male and female percentage
        sex_stats = browser.find_element_by_class_name('studentBody')
        enrolls = iter(sex_stats.find_elements_by_tag_name('dd'))
        enroll_male_percentage = None
        if 'Male' in sex_stats.text:
            enroll_male_percentage = next(enrolls).text
            
        enroll_female_percentage = None
        if 'Female' in sex_stats.text:
            enroll_female_percentage = next(enrolls).text
        
        # race percentage
        enrolls_data = browser.find_element_by_class_name('raace').find_elements_by_tag_name('dd')
        enrolls = iter(enrolls_data)
        
        enroll_americanindiannative_percentage = None
        try:
            browser.find_element_by_class_name('indian')
            enroll_americanindiannative_percentage = next(enrolls).text
        except:
            pass
        
        enroll_asian_pacific_percentage = None
        try:
            browser.find_element_by_class_name('asian')
            enroll_asian_pacific_percentage = next(enrolls).text
        except:
            pass
        
        enroll_black_percentage = None
        try:
            browser.find_element_by_class_name('black')
            enroll_black_percentage = next(enrolls).text
        except:
            pass
        
        enroll_latino_percentage = None
        try:
            browser.find_element_by_class_name('latino')
            enroll_latino_percentage = next(enrolls).text
        except:
            pass
        
        enroll_white_percentage = None
        try:
            browser.find_element_by_class_name('white')
            enroll_white_percentage = next(enrolls).text
        except:
            pass
        
        enroll_towormoreraces_percentage = None
        try:
            browser.find_element_by_class_name('two')
            enroll_towormoreraces_percentage = next(enrolls).text
        except:
            pass
        
        enroll_raceunknown_percentage = None
        try:
            browser.find_element_by_class_name('unknown')
            enroll_raceunknown_percentage = next(enrolls).text
        except:
            pass
        
        enroll_nonresidentalien_percentage = None
        try:
            browser.find_element_by_class_name('alien')
            enroll_nonresidentalien_percentage = next(enrolls).text
        except:
            pass
        
        # attendance percentage
        attend_stats = browser.find_element_by_class_name('attendance')
        enrolls = iter(attend_stats.find_elements_by_tag_name('dd'))
        fulltime_percentage = next(enrolls).text
        
        parttime_percentage = None
        try:
            parttime_percentage = next(enrolls).text
        except:
            pass
        
        print (year,
            school_id,
            overall_rank,
            student_population,
            undergrad_population,
            student_faculty_ration,
            annual_cost,
            in_state_tuition,
            out_state_tuition,
            financial_aid_percentage,
            admission_percentage,
            sat_range,
            act_range,
            financial_grade,
            enroll_male_percentage,
            enroll_female_percentage,
            enroll_americanindiannative_percentage,
            enroll_asian_pacific_percentage,
            enroll_black_percentage,
            enroll_latino_percentage,
            enroll_white_percentage,
            enroll_towormoreraces_percentage,
            enroll_raceunknown_percentage,
            enroll_nonresidentalien_percentage,
            fulltime_percentage,
            parttime_percentage)
        
        #try:
        x.execute('''insert into school_infor_%s (
        id,
        overall_rank,
        student_population,
        undergrad_population,
        student_faculty_ration,
        annual_cost,
        in_state_tuition,
        out_state_tuition,
        financial_aid_percentage,
        admission_percentage,
        sat_range,
        act_range,
        financial_grade,
        enroll_male_percentage,
        enroll_female_percentage,
        enroll_americanindiannative_percentage,
        enroll_asian_pacific_percentage,
        enroll_black_percentage,
        enroll_latino_percentage,
        enroll_white_percentage,
        enroll_towormoreraces_percentage,
        enroll_raceunknown_percentage,
        enroll_nonresidentalien_percentage,
        fulltime_percentage,
        parttime_percentage
        )
        values (
            %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s
        )''' % year, 
        (school_id,
        overall_rank,
        student_population,
        undergrad_population,
        student_faculty_ration,
        annual_cost,
        in_state_tuition,
        out_state_tuition,
        financial_aid_percentage,
        admission_percentage,
        sat_range,
        act_range,
        financial_grade,
        enroll_male_percentage,
        enroll_female_percentage,
        enroll_asian_pacific_percentage,
        enroll_black_percentage,
        enroll_latino_percentage,
        enroll_white_percentage,
        enroll_towormoreraces_percentage,
        enroll_raceunknown_percentage,
        enroll_nonresidentalien_percentage,
        fulltime_percentage,
        parttime_percentage,
        ))
        conn.commit()
        print 'one row inserted'
        
        

if __name__ == '__main__':
    crawl_school_list()