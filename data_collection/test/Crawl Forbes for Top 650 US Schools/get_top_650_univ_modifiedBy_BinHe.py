from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
import time
import codecs
import pdb
import csv
import sys

class crawler:
    def crawl_university(self,browser,output_f,page):
        
        url = 'http://www.forbes.com/top-colleges/list/'
        browser.get(url)
        print 'url expected to crawl: ', url

        #time.sleep(30)
        try: 
            WebDriverWait(browser,40).until(EC.title_contains('Top'))
            
            assert 'America\'s Top Colleges List - Forbes' in browser.title
            print 'current url = ', browser.current_url.encode('utf-8')
            #pdb.set_trace()
            
            # go to disired page number
            print 'Opening page ', page, '...'
            if int(page) >1:
                page_xpath = "/html/body/div[5]/section[2]/div[2]/nav/ul/li[%s]/a"%page
                click_page = browser.find_element_by_xpath(page_xpath)
                click_page.click()
                
                browser.implicitly_wait(30)
                expected_url = 'http://www.forbes.com/top-colleges/list/#page:%s_sort:'%page +'0_direction:asc_search:_filter:All%20states'
                assert browser.current_url == expected_url
                #pdb.set_trace()
                #page_source = browser.page_source
                #print page_source

            
            # get detailed school info from this page and write into output_f
            
            try:
                school_table = browser.find_element_by_xpath('/html/body/div[5]/section[2]/div[2]')
                table = school_table.find_element_by_tag_name('table')
                tbody = table.find_element_by_tag_name('tbody')
                table_row = tbody.find_elements_by_tag_name('tr')
                
                #tbody_2 = table.find_element_by_id('listbody')
                #table_row = tbody_2.find_elements_by_tag_name('tr')
                
                with open(output_f,'w') as writer:
                    writer.write('\r\n')
                    for each_univ in table_row:
                        try:
                            #pdb.set_trace()
                            counter = 0
                            table_cells = each_univ.find_elements_by_tag_name('td')
                            for td in table_cells:
                                if counter == 1:
                                    univ_url = each_univ.find_element_by_tag_name('a').get_attribute('href')
                                    print 'university_url = ', univ_url
                                    univ_name = each_univ.find_element_by_tag_name('h3').text
                                    #print 'university = ', university
                                    #writer.write(university.encode('utf-8')+'\r\n')
                                    content = univ_url + '\r\n'+ univ_name.encode('utf-8')
                                else:    
                                    content = td.text
                                writer.write(content+'\r\n')
                                #print 'write content to %s'%output_f
                                counter += 1
                        except:
                            print 'failed to catch the elements'
                        writer.write('\r\n')    
            except:
                print 'university table does not exist'
        except:
            print 'either timeout or the url changed, please double check the website address'

        
    
            
    def batch_proc(self, page):
        driver = webdriver.Firefox()
        
        #driver = webdriver.Chrome()
        file_name = 'top_university_%s.txt'%page
        self.crawl_university(driver, file_name, page)
        
        driver.quit()
        
if __name__ == '__main__':
    #if len(sys.argv) >1:
    #    page = sys.argv[1]    
    #else:
    #    page = '1'
    
    example = crawler()
    for i in range (1, 8):
        page = i
        example.batch_proc(page)
    print 'crawl finished'
    
    
