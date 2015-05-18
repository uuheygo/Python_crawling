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

def get_bd_index_all_mechanize(file_name):
    
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
    f_error = open('errors_' + st, 'w')
    f_success = open('success_' + st, 'w')
    
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
                if len(school) > 4:
                    target_en = school[2] + school[4]
                else:
                    target_en = school[2]
                target_en = string.replace(target_en, ' ', '%20')
                target_ch = "\"" + school[3] + "\""
                target_ch = string.replace(target_ch, ' ', '%20')
                site = 'site:' + school[1]
                print target_ch, target_en, site
                
                
                # baidu search
                # ch
                url = 'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=' \
<<<<<<< HEAD
                    +target_ch
                url = url.encode('utf8')
                print url
                response = urllib2.urlopen(url, timeout = 10)
=======
                    + target_en + '&rsv_enter=1&rsv_sug3=5&rsv_sug4=745&rsv_sug1=1&' \
                    + 'rsv_sug2=0&inputT=811'
                response = urllib2.urlopen(url, timeout = 20)
>>>>>>> origin/master
                response_html = response.read()
                soup = BeautifulSoup(response_html)
                bs_html = soup.body.prettify(encoding='utf-8')
                target = soup.find('div', {'class': 'nums'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
                # baidu search
                # en
                url = 'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=' \
                    + target_en
                print url
                response = urllib2.urlopen(url, timeout = 20)
                response_html = response.read()
                soup = BeautifulSoup(response_html)
                bs_html = soup.body.prettify(encoding='utf-8')
                target = soup.find('div', {'class': 'nums'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
                # baidu news
                # ch
<<<<<<< HEAD
                url = 'http://news.baidu.com/ns?cl=2&rn=20&tn=news&word='+target_ch
=======
                target_ch = "\"" + school[2] + "\""
                target_ch = string.replace(target_ch, ' ', '%20')
                url = 'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=' \
                    +target_ch+'&rsv_enter=1&rsv_sug3=5&rsv_sug4=745&rsv_sug1=1&' \
                    +'rsv_sug2=0&inputT=811'
>>>>>>> origin/master
                url = url.encode('utf8')
                print url
                response = urllib2.urlopen(url, timeout = 10)
                response_html = response.read()
                soup = BeautifulSoup(response_html)
                bs_html = soup.body.prettify(encoding='utf-8')
                target = soup.find('span', {'class': 'nums'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
                
                # baidu news
<<<<<<< HEAD
                # en
                url = 'http://news.baidu.com/ns?cl=2&rn=20&tn=news&word='+target_en
=======
                # ch
                url = 'http://news.baidu.com/ns?cl=2&rn=20&tn=news&word='+target_ch
                url = url.encode('utf8')
>>>>>>> origin/master
                print url
                response = urllib2.urlopen(url, timeout = 10)
                response_html = response.read()
                soup = BeautifulSoup(response_html)
                bs_html = soup.body.prettify(encoding='utf-8')
                target = soup.find('span', {'class': 'nums'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
                # baidu site
                url = 'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=' \
                    + site
                print url
                response = urllib2.urlopen(url, timeout = 20)
                response_html = response.read()
                soup = BeautifulSoup(response_html)
                bs_html = soup.body.prettify(encoding='utf-8')
                target = soup.find('div', {'class': 'nums'})
                all_txt = target.text
                str_txt = unicodedata.normalize('NFKD', all_txt).encode('ascii','ignore')
                nums_en_index = re.findall(r'\d+', str_txt)
                nums.append(''.join(nums_en_index))
                
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
    get_bd_index_all_mechanize('school_ch_name_v3.csv')