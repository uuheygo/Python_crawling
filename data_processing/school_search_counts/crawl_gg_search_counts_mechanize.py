import mechanize
from time import sleep
import random
import math
import unicodedata
import re
import sys
import codecs
import datetime
import time
from bs4 import BeautifulSoup
import string
import urllib2

# input file has 5 column: id, url, en_name, ch_name, location(optional)

def get_gg_index_all_mechanize(file_name):
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
#     f_error = open('errors_' + st, 'w')
#     f_success = open('success_' + st, 'w')
    
    all_schools = []
    with codecs.open(file_name, 'r', 'utf-8') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            all_schools.append(line)
    #print all_schools
    
    for school in all_schools[0:]:
        sleep(random.random() * 2)
        
        for i in range(5):
            nums = []
            print school, nums
            try:
                # gg search
                # en
                if len(school) > 4:
                    target_en = school[2] + school[4]
                else:
                    target_en = school[2]
                
                br = mechanize.Browser()
                br.set_handle_robots(False)     # ignore robots
                br.set_handle_refresh(False)    # can sometimes hang without this
                br.set_handle_redirect(True)
                br.set_handle_referer(True)
                br.addheaders = [('user-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
                url = "http://www.google.com"
                search_box='q'
                
                br.open(url)
                htmlFile = br.response()
                br.select_form(nr=0)
                br.form[search_box] = target_en
                print target_en
                response = br.submit()
                #response_html = response.get_data()
                soup = BeautifulSoup(response)
                target = soup.find('div', {'id': 'resultStats'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
                # gg hk
                # en
                br = mechanize.Browser()
                br.set_handle_robots(False)     # ignore robots
                br.set_handle_refresh(False)    # can sometimes hang without this
                br.set_handle_redirect(True)
                br.set_handle_referer(True)
                br.addheaders = [('user-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
                url = "http://www.google.com.hk"
                search_box='q'
                
                br.open(url)
                htmlFile = br.response()
                br.select_form(nr=0)
                br.form[search_box] = target_en
                print target_en
                response = br.submit()
                #response_html = response.get_data()
                soup = BeautifulSoup(response)
                target = soup.find('div', {'id': 'resultStats'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
                
                # gg news
                # en
                br = mechanize.Browser()
                br.set_handle_robots(False)     # ignore robots
                br.set_handle_refresh(False)    # can sometimes hang without this
                br.set_handle_redirect(True)
                br.set_handle_referer(True)
                br.addheaders = [('user-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
                url = "http://news.google.com"
                search_box='q'
                
                br.open(url)
                htmlFile = br.response()
                br.select_form(nr=0)
                br.form[search_box] = target_en
                print target_en
                response = br.submit()
                #response_html = response.get_data()
                soup = BeautifulSoup(response)
                target = soup.find('div', {'id': 'resultStats'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
                
                # gg site
                site = 'site:' + school[1]
                br = mechanize.Browser()
                br.set_handle_robots(False)     # ignore robots
                br.set_handle_refresh(False)    # can sometimes hang without this
                br.set_handle_redirect(True)
                br.set_handle_referer(True)
                br.addheaders = [('user-agent','Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3')]
                url = "http://www.google.com"
                search_box='q'
                
                br.open(url)
                htmlFile = br.response()
                br.select_form(nr=0)
                br.form[search_box] = site
                print target_en
                response = br.submit()
                #response_html = response.get_data()
                soup = BeautifulSoup(response)
                target = soup.find('div', {'id': 'resultStats'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
                # write to file
                one_line = school[0] + '\t' + '\t'.join(nums)
                f_success.write(one_line + '\n')
                f_success.flush()
                print one_line
                break
                
            except Exception:
                print sys.exc_info()
                f_error.write(school[0] + '\t' + school[2] + '\n')
                print '\t'.join(school) + '\n'
                f_error.flush()
                pass
    f_error.close()
    f_success.close()
    
if __name__ == '__main__':
    get_gg_index_all_mechanize('school_ch_name_v3.csv')