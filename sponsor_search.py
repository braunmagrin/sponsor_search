# coding: utf-8

import os
import time
import requests
from bs4 import BeautifulSoup


sponsor_dir = 'sponsors'
try:
    os.mkdir(sponsor_dir)
except FileExistsError:
    pass


url_template = 'https://www.kaggle.com/jobs/{}'


for job_number in range(16500, 17100):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print(now, '- Job', job_number, '... ', end='')

    url = url_template.format(job_number)
    res = requests.get(url)

    if not res.ok:
        print('Not OK ({})'.format(res.status_code))
        continue

    soup = BeautifulSoup(res.text, 'html.parser')
    content = soup.find('div', attrs={'class': 'jobs-board-post-content'})

    if not 'Python' in content.text or 'python' in content.text:
        print('No Python')
        continue

    title = '{}_{}'.format(job_number, soup.title.text.split('|')[0]
                                       .split('(')[0]
                                       .replace(' ', '')
                                       .replace('/', ''))
    filename = title + '.txt'
    try:
        apply_link = content.find('p', attrs={'class': 'apply-button'}).a.attrs['href']
    except AttributeError:
        apply_link = '-'

    with open(os.path.join(sponsor_dir, filename), 'w') as f:
        f.write('\n'.join(['Title: {}'.format(soup.title.text),
                           'Original URL: {}'.format(url),
                           'Link: {}'.format(apply_link),
                           content.text]))
    print('OK')

