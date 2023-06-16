# -*- coding: utf-8 -*-
from datetime import datetime
import csv     
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup 
# import sys
import urllib3
import ast

# reload(sys)
# sys.setdefaultencoding('utf8')
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
})

urllib3.disable_warnings()
social = []
scraper_api = 'http://api.scraperapi.com/?api_key=ca84821e129c127233af3f9f1562950f&url='


def indeed_scraper(keyword, location):
    csv.register_dialect('myDialect1',
        quoting=csv.QUOTE_ALL,
        skipinitialspace=True)
    dateTimeObj = datetime.now()
    
    write_file = open('{}+{}.csv'.format(location, keyword), 'w')
    csv_writer = csv.writer(write_file, dialect='myDialect1')
    csv_writer.writerow(["Title","Company","City","State","Zipcode","PostedDateText", "Remote", "Job Shelf" ,"Job Type","Job Link"])
    
    url = 'https://www.indeed.com/jobs?q={}&l={}'.format(keyword, location)
    try:
        r = session.get(url)
    except requests.ConnectionError as e:
        print("Connection failure : " + str(e))
        print("Verification with InsightFinder credentials Failed")
    # html = open('1.html', 'a')
    # html.write(r.text)
    soup = BeautifulSoup(r.text, features="html.parser")

    total_count = soup.find('div', {'id': 'searchCountPages'}).text.split('of')[1].replace('jobs', '').strip()
    if not soup.find('div', {'id': 'searchCountPages'}):
        return
    total_count = int(total_count)
    count = 0
    print('{}+{}.csv'.format(location, keyword), total_count)
    while True:
        print('======================={}========================='.format(count))
        url = 'https://www.indeed.com/jobs?q={}&l={}&start={}'.format(keyword, location, count)
        try:
            r = session.get(url)
        except requests.ConnectionError as e:
            print("Connection failure : " + str(e))
            print("Verification with InsightFinder credentials Failed")
        # html = open('1.html', 'a')
        # html.write(r.text)
        soup = BeautifulSoup(r.text, features="html.parser")
        jobs = soup.findAll('div', class_='jobsearch-SerpJobCard')
        for job in jobs:
            title = ''
            job_url = ''
            if job.find('h2', class_='title'):
                title = job.find('h2', class_='title').text.strip()
                job_url = job.find('h2', class_='title').find('a').attrs['href']
            company = ''
            if job.find('span', class_='company'):
                company = job.find('span', class_='company').text.strip()

            address = ''
            if job.find('div', class_='location'):
                address = job.find('div', class_='location').text.strip()
            address = address.split('(')[0]
            city = ''
            state = ''
            zipcode = ''
            if len(address.split(',')) == 2:
                city = address.split(',')[0].strip()
                if len(address.split(',')[1].strip().split(' ')) > 1:
                    state = address.split(',')[1].strip().split(' ')[0]
                    zipcode = address.split(',')[1].strip().split(' ')[1]
            postedDateText = ''
            if job.find('span', class_='date'):
                postedDateText = job.find('span', class_='date').text
            
            remote = ''
            if job.find('span', class_='remote'):
                remote = job.find('span', class_='remote').text.strip()
            
            job_shelf = ''
            for item in job.findAll('td', class_='jobCardShelfItem'):
                if job_shelf == '':
                    job_shelf = item.text.strip()
                else:
                    job_shelf = job_shelf + ', ' + item.text.strip()
            
            salary = ''
            if job.find('span', class_='salaryText'):
                salary = job.find('span', class_='salaryText').text.strip()
            
            try:
                r = session.get('https://www.indeed.com' + job_url)
            except requests.ConnectionError as e:
                print("Connection failure : " + str(e))
                print("Verification with InsightFinder credentials Failed")
            # html = open('1.html', 'a')
            # html.write(r.text)
            soup = BeautifulSoup(r.text, features="html.parser")

            job_type = ''
            if soup.find('div', class_='jobsearch-jobDescriptionText'):
                for item in soup.find('div', class_='jobsearch-jobDescriptionText').findAll('p'):
                    if 'Job Type:' in item.text:
                        job_type = item.text.replace('Job Type:', '').strip().split('Job Posted:')[0]
                        if ':' in job_type:
                            job_type = ''
                        else:
                            break
            print([title, company, city, state, zipcode, postedDateText, remote, job_shelf , job_type])
            csv_writer.writerow([title, company, city, state, zipcode, postedDateText, remote, job_shelf , job_type, 'https://www.indeed.com' + job_url])
        count = count + 10
        if count >= total_count:
            break


cities = [
    'Denver',
    'Colorado Springs',
    'Phoenix',
    'Austin',
    'San Diego',
    'Seattle',
    'Las Vegas', #(Video Editor)
    'Atlanta',
    'Dallas'
]
keywords = [
    'SEO',
    'Search Engine Optimization',
    'Search Engine Marketing',
    'SEM',
    'Digital Marketing',
    'Video Editor'
]
for city in cities:
    for keyword in keywords:
        indeed_scraper(keyword, city)

#         # monster_scraper(keyword, sys.argv[1:][0].replace('/',' '))
