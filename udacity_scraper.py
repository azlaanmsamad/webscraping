from bs4 import BeautifulSoup
import requests
import pandas as pd

urls = ['school-of-ai', 'school-of-data-science', 'school-of-cloud-computing', 'school-of-programming', 'school-of-autonomous-systems', 'school-of-business'] 

def initialise_dict():
    data_dict = {}
    data_dict['Title'] = []
    data_dict['URL'] = []
    return data_dict

for i in urls:
    topicurls = 'https://www.udacity.com/courses/' + i
    coursename = 'udacity_' + i.split('-')[-1] + '.pkl'
    search_source = requests.get(topicurls).content
    search_soup = BeautifulSoup(search_source, 'lxml')
    data_dict = initialise_dict()
    for courses in search_soup.find_all('div', class_='card-content'):
        data_dict['Title'].append(courses.a.text)
        link = 'https://www.udacity.com' + courses.a['href']
        data_dict['URL'].append(link)
    data = pd.DataFrame.from_dict(data_dict)
    data.to_pickle(coursename)
    print(data)


