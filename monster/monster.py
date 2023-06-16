# -*- coding: utf-8 -*-
from datetime import datetime
import csv     
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup 
import sys
import urllib3
import ast

reload(sys)
sys.setdefaultencoding('utf8')

urllib3.disable_warnings()
social = []
scraper_api = 'http://api.scraperapi.com/?api_key=ca84821e129c127233af3f9f1562950f&url='
def monster_scraper(keyword, location):
    
    csv.register_dialect('myDialect1',
        quoting=csv.QUOTE_ALL,
        skipinitialspace=True)
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%Y_%m_%d_%H_%M_%S")
    print('{}+{}_{}.csv'.format(location, keyword, timestampStr))
    write_file = open('{}+{}.csv'.format(location, keyword), 'w')
    csv_writer = csv.writer(write_file, dialect='myDialect1')
    csv_writer.writerow(['Title', 'Company', 'City', 'State', 'Zipcode', 'PostedDateText', 'PostedDate', 'Job Type', 'Job Link', 'Year Founded', 'Company Size', 'Website', 'Industry', 'Twitter', 'Facebook', 'Instagram', 'YouTube'])
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    })
    url = 'https://www.monster.com/jobs/search/?q={}&where={}'.format(keyword, location)
    try:
        r = session.get(url)
    except requests.ConnectionError, e:
        print("Connection failure : " + str(e))
        print("Verification with InsightFinder credentials Failed")
    # html = open('1.html', 'a')
    # html.write(r.text)
    soup = BeautifulSoup(r.text, features="html.parser")
    print(soup.find('header', class_='title').find('h2').text.strip().split('(')[1].split(' ')[0])
    total_count = int(soup.find('header', class_='title').find('h2').text.strip().split('(')[1].split(' ')[0])
    page_count = 1
    while True:
        print('-----------------------{}------------------------------'.format(page_count))
        api_url = 'https://www.monster.com/jobs/search/pagination/?q={}&where={}&isDynamicPage=true&isMKPagination=true&page={}'.format(keyword, location, page_count)
        try:
            r = session.get(api_url)
        except requests.ConnectionError, e:
            print("Connection failure : " + str(e))
            print("Verification with InsightFinder credentials Failed")
        jobs = json.loads(r.text)
        for job in jobs:
            if 'Title' not in job: continue
            title = job['Title']
            link = job['JobViewUrl']
            postedText = job['DatePostedText']
            postedDate = job['DatePosted']
            location = job['LocationText']
            
            city = location.split(',')[0].strip()
            state = ''
            if len(location.split(',')) > 1:
                state = location.split(',')[1].strip()

            zipcode = ''
            if len(location.split(',')) > 2:
                zipcode = location.split(',')[2].strip()

            company = job['Company']['Name']

            try:
                r = session.get(link)
            except requests.ConnectionError, e:
                print("Connection failure : " + str(e))
                print("Verification with InsightFinder credentials Failed")
            soup = BeautifulSoup(r.text, features="html.parser")
            summaries = soup.findAll('div', class_='font-semibold')
            jobType = ''
            for summary in summaries:
                if summary.attrs['name'] == 'value_job_type':
                    jobType = summary.text.strip()
            jobType = jobType.replace('fulltime', 'Full Time').replace('contract', 'Temporary/Contract/Project').replace('employee', 'Employee')
            print('==============================================')
            

            jobKey = job['MusangKingId']
            company_api = '{}https://job-openings.monster.com/v2/job/pure-json-view?Js30Flow=%7B%22searchPath%22:%22%22,%22q%22:%22{}%22,%22where%22:%22{}%22,%22useLpfRootPrefix%22:true,%22sequence%22:1%7D&jobid={}&callback=jQuery33107051459195617071_1588273076738'.format(scraper_api, keyword, location, jobKey)
    
            try:
                r = session.get(company_api)
            except requests.ConnectionError, e:
                print("Connection failure : " + str(e))
                print("Verification with InsightFinder credentials Failed")
            # print(r.text)
            detail = r.text
            detail = detail.encode('utf-8')
            
            detail = detail.rstrip(')')
            detail = detail.replace('jQuery33107051459195617071_1588273076738(', '')
            detail = json.loads(detail)
            
            founded = ''
            industry = ''
            website = ''
            size = ''
            medias = {
                'twitter': '',
                'facebook': '',
                'instagram': '',
                'youtube': ''
            }
            # twitter = ''
            # facebook = ''
            # linkedIn = ''

            if 'companyInfo' in detail:
                company_info = detail['companyInfo']
                if 'yearFounded' in company_info:
                    if company_info['yearFounded'] == 0:
                        founded = ''
                    else:
                        founded = company_info['yearFounded']
                if 'websiteUrl' in company_info:
                    website = company_info['websiteUrl']
                if 'industryName' in company_info:
                    industry = company_info['industryName']
                if 'companySizeName' in company_info:
                    size = company_info['companySizeName']
                if 'followMediaLinks' in company_info:
                    links = company_info['followMediaLinks']
                    for media in links:
                        if 'http' not in media['url']:
                            medias[media['name']] = 'https:' + media['url']
                        else:
                            medias[media['name']] = media['url']
                        if media['name'] not in social:
                            social.append(media['name'])
            print(title, link, postedText, postedDate, city, state, zipcode, jobType, company, founded, size, website, industry, medias['twitter'], medias['facebook'], medias['instagram'], medias['youtube'])
            print(social)
            csv_writer.writerow([title, company, city, state, zipcode, postedText, postedDate, jobType, founded, size, website, link])
        if page_count * 25 > total_count:
            break
        page_count = page_count + 1
    # soup = BeautifulSoup(r.text, features="html.parser")
    # print(r.text)
cities = [
   # 'Denver',
   # 'Colorado Springs',
    # 'Phoenix',
     'Austin',
#     'San Diego',
 #    'Seattle',
  #   'Las Vegas',
   #  'Atlanta',
    # 'Dallas'
]
keywords = [
 #    'SEO',
  #   'Search Engine Optimization',
   #  'Search Engine Marketing',
     'SEM',
    'Digital Marketing',
    'Video Editor'
]
for city in cities:
    for keyword in keywords:
        monster_scraper(keyword, city)

        # monster_scraper(keyword, sys.argv[1:][0].replace('/',' '))



