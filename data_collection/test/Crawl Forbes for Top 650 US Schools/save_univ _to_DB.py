
import sys
import MySQLdb
''' after crawl new rank list from http://www.forbes.com/top-colleges/list/
using get_top_650_univ_modifiedBy_BinHe.py.  Seven text files are generated:
top_university_(1-7).txt
This script is to save the information in those text files into databases'''

def connect_to_DB():
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
		user="mediaWatch", # your username
		passwd="Morefruit2013", # your password
		db="mediaWatch",
		use_unicode=True,
		charset="utf8") # name of the data base
    return db

def read_top_university_file(file_number):
    file_to_read = 'top_university_%s.txt'%file_number
    with open(file_to_read, 'r') as reader:
        line_count = 0
        over_all_list = {}
        for eachline in reader:
            content = eachline.strip().replace('\r','').replace('\n','')
            if (line_count == 0):
                school = {}
            else:
                if content =='':

                    if line_count != 7: # this means there is an error in the file for read
                        print 'line_count is %s for school #%s, please check the orginal file'%(line_count, rank)

                    else: # the past block contains 7 lines
                        over_all_list[rank] = school
                     # reset line_count and school
                    line_count =0
                    school = {}

                else:
                    try:
                        if (line_count == 1):
                            rank = content
                            school['rank'] = content
                        elif (line_count  == 2):
                            school['detail_url'] = content
                        elif (line_count  == 3):
                            school['name'] = content
                        elif (line_count  == 4):
                            school['state'] = content
                        elif (line_count  == 5):
                            ## be careful of unavailable cost information which value is 'N/A'
                            school['cost'] = content.replace('$','').replace(',','')
                        else: #  (line_count == 6):
                            ## be careful of unavailable population information which value is 'N/A'
                            school['total_student'] = content.replace(',','')
                    except:
                        print 'There might be errors for school#%s'%rank
            line_count += 1
    reader.close()
    return over_all_list

def batch_proc(file_number):
    over_all_list = read_top_university_file(file_number)
    db = connect_to_DB()
    cur = db.cursor()
    try:
        for key in over_all_list:
            rank = int(key)
            school_info = over_all_list[key]
            url = school_info['detail_url']
            name = school_info['name']
            state = school_info['state']
            sql = 'insert into overall_school_list value (default, %s, %s, %s, %s)'
            cur.execute(sql, (name, url, state, rank))
            db.commit()
    except Exception, e:
        print e


if __name__ == '__main__':
    #file_number = sys.argv[1]
    file_number = 1
    batch_proc(file_number)
    #over_all_list = read_top_university_file(file_number)


