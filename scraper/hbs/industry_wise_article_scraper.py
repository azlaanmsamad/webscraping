from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from stem import Signal
from stem.control import Controller
import time
import logging
import threading
import csv
import os
import pandas as pd
import pdb, re

def switchIP():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

def my_proxy(PROXY):
    # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
    chrome_dir_path = os.getcwd() + '/chromedriver.exe'
    options = Options()
    options.headless = True
    options.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Chrome(options=options, executable_path=chrome_dir_path)
    path = os.path.join(os.getcwd(), 'geckodriver')
    return webdriver.Firefox(options=options, firefox_profile=fp, executable_path=path)

def dict_intialiser():
    headers = ['Title', 'Url', 'Date', 'Summary']
    data_dict = {}
    for i in headers:
        data_dict[str(i)] = []
    return data_dict

def crawl_and_save(driver, data_dict, page_num, industry_name):
    
    current_page = page_num
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    main_page_articles = soup.find_all('article', attrs={'class': re.compile('^item-list item')})

    for i in main_page_articles:
        #Append the date to the dict
        article = i.find('h2', "post-title")
        #Find the next <a> tag containing information about the article.
        url = article.a['href']
        Title = article.a.get_text()

        data_dict['Url'].append(url)
        data_dict['Title'].append(Title)
        
        date = i.find('p', 'post-meta').find_next('span', 'tie-date').get_text()
        data_dict['Date'].append(date)

        summary = i.find('div','entry')
        data_dict['Summary'].append(summary.p.get_text())

    if current_page < 40:
        try:
            webpage = 'https://www.electronicsweekly.com/news/page/' + str(current_page+1)
            driver.get(webpage)
            #button = driver.find_element_by_xpath("//span[@id='tie-next-page']")
            #element.send_keys()
            #driver.implicitly_wait(10)
            #webdriver.ActionChains(driver).move_to_element(button).click(button).perform()
            print('On page  {} now.'.format(current_page+1))
        except IndexError:
            df = pd.DataFrame(data_dict)
            print(df.head())
            print(df.shape)
            savePath = os.getcwd() + '/datasets/second/' + industry_name + '.csv'
            df.to_csv(savePath)
            return data_dict
    else:
        df = pd.DataFrame(data_dict)
        df['Industry'] = 'Electroncs'
        print(df.head())
        print(df.shape)
        savePath = os.getcwd() + '/datasets/second/' + industry_name + '.csv'
        df.to_csv(savePath)
        return data_dict
    '''else:
        try:
            driver.find_elements_by_xpath("//a[@class='ink facetctrl-ajax-page-link']")[1].click()
            print('On page {} now'.format(current_page + 1))
        except IndexError:
            print('Reached the last page of the website')
            df = pd.DataFrame(data_dict)
            print(df.head())
            savePath = os.getcwd() + '/datasets/' + industry_name + '.csv'
            print(df.shape)
            df.to_csv(savePath)
            return data_dict'''

    next_page = current_page + 1
    crawl_and_save(driver, data_dict, next_page, industry_name)
    return data_dict

def main_execution(url, industry_name):
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('disable-extensions')
    #chrome_options.add_argument('--start-maximized')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    #chrome_options.add_argument("--remote-debugging-port=9222")
    #driver = my_proxy(PROXY)
    chrome_dir_path = os.getcwd() + '/chromedriver.exe'
    driver = webdriver.Chrome(chrome_dir_path, chrome_options=chrome_options)
    driver.get(url)
    #driver.implicitly_wait(100)
    data_dict = dict_intialiser()
    page_number = 1
    #for i in range(10):
    #scroll(driver, 5)
    ## Accept cookies
    #pdb.set_trace()
    #driver.find_element_by_xpath("//button[@title='Accept Cookies']").click()
    ## Checking the condition if its a last page
    data_dict = crawl_and_save(driver, data_dict, page_number, industry_name)
    ## find_elements_by_xpath returns all the elements, as oppose to element_by_xpath which
    ## return just the first encountered element.
    ## to get text in selenium replace ".click()" with ".text"
    ##driver.find_elements_by_xpath("//a[@class='ink facetctrl-ajax-page-link facetctrl-scroll-top]")
    ##                             [1].click()


def scroll(driver, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(1):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time + (0.01*i))

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        #print(i, end='\r')
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height



if __name__ == "__main__":

    url = "https://www.electronicsweekly.com/news/"
    #url = "https://hbswk.hbs.edu/Pages/browse.aspx?HBSIndustry=Green%20Technology&HBSIndustry=Energy"
    #https://hbswk.hbs.edu/Pages/browse.aspx?HBSIndustry=Construction
    main_execution(url, 'Electroncs_weeklydotcom')

    ## NOTES ABOUT THE DATASETS:
    """TechnologyRemove Technology → TelecommunicationsRemove Telecommunications → Media & BroadcastingRemove Media & Broadcasting → Motion Pictures & VideoRemove Motion Pictures & Video → MusicRemove Music → InformationRemove Information → Information TechnologyRemove Information Technology → Video GameRemove Video Game → Web ServicesRemove Web Services → Entertainment & RecreationRemove Entertainment & Recreation → ComputerRemove Computer → Communications"""
    """Electric power and Natural Gas contains: Green Tech and Energy"""
    """Financial Services: financial services, Legal services, INsurance, Banking, Accounting"""
    """Consumer ProductsRemove Consumer Products → FashionRemove Fashion → Food & BeverageRemove Food & Beverage → RetailRemove Retail → Beauty & CosmeticsRemove Beauty & Cosmetics"""
    """Put Education under the Public and Social Sector"""
