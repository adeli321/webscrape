#! /usr/bin/python3

import requests
import datetime
import lxml
from bs4 import BeautifulSoup
from postgres_connect import UsePostgres

db_config = {'host': 'localhost', 
            'user': 'anthonydelivanis', 
            'database': 'anthonydelivanis'}

url       = ['https://www.indeed.com/jobs?q=Junior+Data+Engineer&l=', 
            'https://www.indeed.com/jobs?q=Junior+Data+Engineer&start=10', 
            'https://www.indeed.com/jobs?q=Junior+Data+Engineer&start=20', 
            'https://www.indeed.com/jobs?q=Junior+Data+Engineer&start=30']

url2      = ['https://www.indeed.com/jobs?q=Data+Engineer&l=', 
            'https://www.indeed.com/jobs?q=Data+Engineer&start=10', 
            'https://www.indeed.com/jobs?q=Data+Engineer&start=20', 
            'https://www.indeed.com/jobs?q=Data+Engineer&start=30']

for i in url2:
    timestamp = datetime.datetime.now()
    page      = requests.get(i)
    soup      = BeautifulSoup(page.text, 'lxml')

    job_names = soup.find_all('a', class_='jobtitle')

    job_links = []
    for i in range(len(job_names)):
        job_links.append(job_names[i]['href'])

    with UsePostgres(db_config) as cursor:
        for i in job_links:
            new_job  = requests.get('https://www.indeed.co.uk' + i)
            new_soup = BeautifulSoup(new_job.text, 'lxml')
            try:
                summary  = new_soup.find('div', id='jobDescriptionText').text
            except AttributeError as err:
                summary = None
            title    = new_soup.find('h3').text
            comp_loc = new_soup.find('div', 'jobsearch-InlineCompanyRating').text
            split    = comp_loc.split('-')
            company  = split[0]
            location = split[1]
            cursor.execute("""INSERT INTO job_listings(title, company, location, summary, timestamp) 
                            VALUES(%s, %s, %s, %s, %s)""", 
                            (title, company, location, summary, timestamp))


# google_api_key = 'AIzaSyDDPQDF7E6gWlHMlbTUF5ECTiZw9JVdX9U'
# https://maps.googleapis.com/maps/api/geocode/json?address=London&key=AIzaSyDDPQDF7E6gWlHMlbTUF5ECTiZw9JVdX9U

