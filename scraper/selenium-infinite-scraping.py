from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
import time
import logging
import threading
import csv
import os


def switchIP():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

def my_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks",PROXY_HOST)
    fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))
    fp.update_preferences()
    options = Options()
    options.headless = True
    path = os.path.join(os.getcwd(), 'geckodriver')
    return webdriver.Firefox(options=options, firefox_profile=fp, executable_path=path)

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

def all_links(url):
    print('Thread {} started.'.format(threading.current_thread().name))
    # Setup the driver. This one uses firefox with some options and a path to the geckodriver
    driver = my_proxy("127.0.0.1", 9050)
    # implicitly_wait tells the driver to wait before throwing an exception
    driver.implicitly_wait(30)
    # driver.get(url) opens the page
    driver.get(url)
    # This starts the scrolling by passing the driver and a timeout
    scroll(driver, 5)
    # Once scroll returns bs4 parsers the page_source
    soup_a = BeautifulSoup(driver.page_source, 'lxml')
    # Then we close the driver as soup_a is storing the page source
    driver.close()
    header =['Title', 'Link']
    # Empty array to store the links
    links = []
    with open('{}.csv'.format(threading.current_thread().name), mode='a') as link_dump:
        link_writer = csv.writer(link_dump, delimiter=',')
        link_writer.writerow(header)
        # Looping through all the h1 elements in the page source that contain the classes seen below
        for heading in soup_a.find_all('div', {"class":"fv fw"}):
            # link.get('href') gets the href/url out of the h1 element
            a = heading.find('a')
            title = a.get_text()
            link = a.get('href')
            link_init = "https://medium.com"
            if link.find('https://', 0, 9) == 0:
                link_writer.writerow([title, link])
            else:
                link = link_init + link
                link_writer.writerow([title, link])     

    return


# Medium Topic URLs
url_ai = 'https://www.udemy.com/courses/development/data-science/'
url_ds = 'https://medium.com/topic/data-science'
url_ml = 'https://medium.com/topic/machine-learning'

# Init threads
thread_ai = threading.Thread(target=all_links, name='thread_ai', args=(url_ai,))
'''thread_ds = threading.Thread(target=all_links, name='thread_ds', args=(url_ds,))
thread_ml = threading.Thread(target=all_links, name='thread_ml', args=(url_ml,))'''

# Start threads
thread_ai.start()
#thread_ds.start()
#thread_ml.start()

# Wait for threads to finish
thread_ai.join()
#thread_ds.join()
#thread_ml.join()
