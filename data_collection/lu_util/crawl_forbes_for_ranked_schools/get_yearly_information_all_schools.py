#######################
# What: add yearly information to table school_infor_yearly for each school
# When: updating of yearly information in update_school_list.py fails in the middle
# How: 1. manually set the year
#      3. used to fix failure in update_school_list.py, get the corresponding ids and forbes urls using where clause
#      4. in case of failure in the middle, get the id of failure point, and start from there to finish the process
#######################


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

# update school yearly information for every school(rank, tuition, student's number, etc. could be different)
def update_yearly_infor(year):
    # delete existing table
#     try:
#         x.execute("drop table if exists school_infor_%s" % MySQLdb.escape_string(year))
#         conn.commit()
#         print 'drop existing table'
#     except:
#         print 'table not existing'
#         pass
#         
    # create a table if not existing to store new yearly information
    
#     try:
#         x.execute('''create table school_infor_%s if not exists (
#                 id int not null primary key,
#                 overall_rank int,
#                 student_population varchar(10),
#                 undergrad_population varchar(10),
#                 student_faculty_ration varchar(10),
#                 annual_cost varchar(10),
#                 in_state_tuition varchar(10),
#                 out_state_tuition varchar(10),
#                 financial_aid_percentage varchar(10),
#                 admission_percentage varchar(10),
#                 sat_range varchar(50),
#                 act_range varchar(50),
#                 financial_grade varchar(10),
#                 enroll_male_percentage varchar(10),
#                 enroll_female_percentage varchar(10),
#                 enroll_americanindiannative_percentage varchar(10),
#                 enroll_asian_pacific_percentage varchar(10),
#                 enroll_black_percentage varchar(10),
#                 enroll_latino_percentage varchar(10),
#                 enroll_white_percentage varchar(10),
#                 enroll_towormoreraces_percentage varchar(10),
#                 enroll_raceunknown_percentage varchar(10),
#                 enroll_nonresidentalien_percentage varchar(10),
#                 fulltime_percentage varchar(10),
#                 parttime_percentage varchar(10),
#                 foreign key(id) references school_list(id)
#                 )''' % MySQLdb.escape_string(year))
#         conn.commit()
#         print 'created table school_infor_' + year
#     except:
#         pass
        
    # can add "where" clause in case failed in middle
    starting_num = raw_input('Please enter the starting ID of schools (1 to 650): ')
    x.execute('select id, forbes_url from school_list where id >= %s', (starting_num,))
    
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
        
        print (school_id,
            year,
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
        year,
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
            %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s
        )''' % year, 
        (school_id,
        year,
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
        parttime_percentage,
        ))
        conn.commit()
        print 'one row inserted'
        
        

if __name__ == '__main__':
    year = raw_input('Enter the year of ranking: ')
    update_yearly_infor(year) # find the year mannually
    browser.close()