
import MySQLdb
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
import time
import codecs


""" read general school info from DB. Then crawl detailed school info from Forbes individual school pages. """


def connect_to_DB():
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
		user="mediaWatch", # your username
		passwd="Morefruit2013", # your password
		db="mediaWatch",
		use_unicode=True,
		charset="utf8") # name of the data base
    return db

def read_DB(start=1, end=650):

    """ read general school info from database table overall_school_list """

    db = connect_to_DB()
    cur = db.cursor()
    sql = 'select * from overall_school_list where rank between %s and %s order by rank'
    try:
        cur.execute(sql, (start, end))
        overall_list = cur.fetchall()
        db.close()
        return overall_list

    except MySQLdb.Error, e:
        print e
        return -1

def update_keywords_table():

    """ Everytime after we re_crawl the Forbes top university list from : http://www.forbes.com/top-colleges/list/ ,
    we need to cross exam with our existing school record to see whether there are new schools appear on the top 650 list for the first time.
    before we run this function, it is better to go directly to database and run the sql below to visualize the difference yourself.
    if the change only involves a few schools, it might be easier to just update the Keywords table manually.
    Otherwise this function will help you update the Keywords table with new schools.
    sql:
    SELECT Over.Name, Over.rank, Keywords.Keyword, Keywords.KeywordID FROM overall_school_list as Over
    left join Keywords on Over.Name = Keywords.Keyword
    UNION
    SELECT Over.Name, Over.rank, Keywords.Keyword, Keywords.KeywordID FROM overall_school_list as Over
    right join Keywords on Over.Name = Keywords.Keyword
    where Keywords.category = 'university'
    order by rank
    """

    overall_list = read_DB()
    assert  overall_list != -1
    db = connect_to_DB()
    cur = db.cursor()

    for each_school in overall_list:
        name = each_school[1]
        sql = 'select count(*) from Keywords where Keyword = %s'
        cur.execute(sql, name)
        row = cur.fetchone()
        count = int(row[0])

        if count == 0:
            try:
                sql = 'insert into Keywords value (default, %s, "Active", default, "University")'
                cur.execute (sql, name)
                db.commit()
                assert isinstance(name, object)
                print 'insert %s into Keywords table'%name

            except MySQLdb.Error, e:
                print e
        else:
            print '%s already in database'%name


def crawl_forbes_selenium(start, end):
    """ run update_keywords_table() before this function. Or make sure all school names are saved in the keywords table."""

    overall_list = read_DB(start, end)
    assert  overall_list != -1

    browser = webdriver.Firefox()
    file_name = 'university_detail_%s_to_%s.txt'%(start, end)
    with open (file_name, 'w') as writer:
        for each_school in overall_list:
            try:
                 school_info = univ_detail(each_school)
                 format_file(school_info, writer)
            except:
                print '%s %s is not available, please verify later. '%(each_school[4], each_school[1])
                continue

    writer.close()
    #browser.quit()




def univ_detail(school):
    ''' adapt from Hou Rong's class mothod Crawler.univ_detail()'''
    name = school[1]
    forbes_url = school[2]
    state = school[3]
    rank = school[4]

    #Open a browser by selenium
    browser = webdriver.Firefox()
    browser.get(forbes_url)
    print 'url expected to crawl: ', forbes_url
    school_info ={ 'name':name, 'rank':rank, 'state':state }
    school_info['at_a_glance'] = []
    school_info['forbes_list'] = []

    try:
        WebDriverWait(browser,40).until(EC.title_contains(name))

        assert name in browser.title
        print 'current url = ', browser.current_url.encode('utf-8')

        try:
            #info = browser.find_element_by_css_selector('div section#collegetop')
            address = browser.find_element_by_class_name('profileLeft').find_element_by_class_name('address').find_elements_by_tag_name('li')
            #print 'address found'
            i = 0
            print '############################## contact info ###################################'
            for each in address:
                if  (i > 2):
                    pass
                elif (i == 0):
                    print 'localtion:', each.text
                    school_info['location'] = each.text
                elif (i == 1):
                    print 'tel: ', each.text
                    school_info['tel'] = each.text
                else:
                    print 'website: ', each.text
                    school_info['website'] = each.text
                i += 1

            glance_area = browser.find_element_by_class_name('profileRight').find_element_by_class_name('stats')
            #print 'glance_area found'
            glance_lefts = glance_area.find_element_by_class_name('ataglanz').find_elements_by_tag_name('li')
            #print 'glance_lefts found'
            glance_rights = glance_area.find_element_by_class_name('forbeslists').find_elements_by_tag_name('li')
            #get overall ranking of the school


            print '############################## general info ###################################'
            for each in glance_lefts:
                try:
                    general_info = each.text
                    general_info = general_info.replace('ratioa','ratio').replace('costc','cost').replace('tuitionc','tuition').replace('aidd','aid').replace('admittede','admitted').replace('rangef','range')
                    print general_info
                    school_info['at_a_glance'].append(general_info)
                except:
                    print 'glance_left\'s elements not found'
            print '############################## rank detail ###################################'
            for each in glance_rights:
                try:
                    rank_detail = each.text
                    print rank_detail
                    school_info['forbes_list'].append(rank_detail)
                except:
                    print 'rank detail not found'

        except:
            print 'failed to catch the element'

        print '############################## more detail info #################################'

        school_info['gender'] = []
        school_info['ethnicity'] = []
        school_info['attendance'] = []
        try:
            chart_area = browser.find_element_by_class_name('byTheNumbers')
            #print 'chart_area found'
            student_body = chart_area.find_element_by_class_name('studentBody')
            #print 'student_body found'
            stubod = student_body.find_elements_by_class_name('stuBod')
            for each in stubod:
                gender = each.find_element_by_tag_name('dt').text
                value = each.find_element_by_tag_name('dd').text
                print gender,": ",value
                school_info['gender'].append(gender+": "+value)
            print '==================================================='
            race = chart_area.find_element_by_class_name('raace').find_element_by_class_name('race')
            print 'race found'
            dts = race.find_elements_by_tag_name('dt')
            dds = race.find_elements_by_tag_name('dd')
            for i in range(len(dts)):
                ethnicity = dts[i].text
                value = dds[i].text
                print ethnicity,": ", value
                school_info['ethnicity'].append(ethnicity+": "+value)
            print '==================================================='
            attendance = chart_area.find_element_by_class_name('attendance')
            #print 'attendance found'
            dls = attendance.find_elements_by_class_name('stuBod')
            #print 'dls found'
            for each in dls:
                attend = each.find_element_by_tag_name('dt').text
                value = each.find_element_by_tag_name('dd').text
                print attend,": ", value
                school_info['attendance'].append(attend+": "+value)
            print '==================================================='
            #close browser and return crawled data for each school
            browser.quit()
            return school_info
        except:
            print 'failed to catch chart_area element'
    except:
        print 'either timeout or the url changed, please double check the website address'
        browser.quit()
        return False



def format_file(school_info, writer):
    try:

        writer.write('Rank: '+ str(school_info['rank'])+'\r\n')
        writer.write('Name: '+ school_info['name']+'\r\n')
        writer.write('State: '+ school_info['state']+'\r\n')
        writer.write('Tel: '+ school_info['tel']+'\r\n')
        writer.write('Website: '+ school_info['website']+'\r\n')

        #writer.write('Cost: '+ school_info['cost'])
        #writer.write('Total student population: '+ school_info['total_students'])
        #writer.write('--- At a Glance --- \r\n')
        if school_info['at_a_glance']:
            for each in school_info['at_a_glance']:
                writer.write(each+'\r\n')
        #writer.write('--- Forbes List --- \r\n')
        if school_info['forbes_list']:
            for each in school_info['forbes_list']:
                writer.write(each+'\r\n')
        if school_info['gender']:
            for each in school_info['gender']:
                writer.write(each +'\r\n')
        if school_info['ethnicity']:
            for each in school_info['ethnicity']:
                writer.write(each+'\r\n')
        if school_info['attendance']:
            for each in school_info['attendance']:
                writer.write(each+'\r\n')
        writer.write('############### Next ###############\r\n')
        writer.flush()
        return True
    except:
        print '%s %s can not be written to file'%(school_info['rank'], school_info['name'])




if __name__ == '__main__':
    update_keywords_table()
    crawl_forbes_selenium(501, 650)





