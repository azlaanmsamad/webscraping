# Selenium Tutorials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = '/home/azlaan/chromedriver'
driver = webdriver.Chrome(PATH)

driver.get('https://techwithtim.net')
print(driver.title)


# Searching for the keyword 'test' by finding the input node of HTML page, 's' is the id for the input search bar. RETURN is used to press enter and search for the keyword 'test'.
search = driver.find_element_by_name("s")
search.send_keys('test')
search.send_keys(Keys.RETURN)

# The next line when executed will lead to an error since it taked time to load the search result.
# Therefore we need to make selenium to wait and then look for the keyword 'main' which contains the
# all the search results.

try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )
    print(main.text)
except:
    driver.quit()

time.sleep(5)
driver.quit()
