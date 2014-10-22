#!/usr/bin/env python
import os
import time
import json
from splinter import Browser
from datetime import datetime
# from pymendez import auth
# from pysurvey.util import setup_stop
# setup_stop()

address = 'https://my.t-mobile.com/login/Default.aspx'
outfile = os.path.expanduser('~/data/bandwidth/tmobile_splinter.txt')


with open(os.path.expanduser('~/.limited/tmobile.auth'), 'r') as f:
    user,pw = f.read().strip().split(' ')
# user,pw = auth('tmobile',['username','password'])


driver = 'firefox'
tmp = dict(
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36"
)

# 
with Browser(driver, **tmp) as browser:
    print 'Loading: {}'.format(address)
    browser.visit(address)
    time.sleep(10)
    print 'Here: {}'.format(browser.url)
    browser.find_by_id('Login1_txtMSISDN').first.fill(user)
    # browser.find_by_id('Login1_txtMSISDN').first.type(user, slowly=True)
    
    print 'Sleeping before next step'
    time.sleep(10)
    browser.find_by_id('Login1_txtPassword').first.fill(pw)
    # browser.find_by_id('Login1_txtPassword').first.type(pw, slowly=True)
    
    print 'Sleeping before next step'
    time.sleep(10)
    browser.find_by_id('lnkBtnLogin').first.click()
    
    print 'Sleeping before next step'
    time.sleep(10)
    while True:
        if browser.is_text_present('Welcome,', wait_time=10):
            break
        print 'sleep 1 sec'
        time.sleep(1)
        
    print 'Now: {}'.format(browser.url)
    
    out = []
    for desc,div in zip(browser.find_by_css('div.datausage-mod-date'),
                        browser.find_by_css('div.datausage-mod-desc') ):
        out.append('{} {}'.format(desc.text, div.text.replace('\n','  ')))
    for desc, div in zip(browser.find_by_css('div.myaccount-mod-date'),
                         browser.find_by_css('div.myaccount-mod-desc') ):
        out.append('{} {}'.format(desc.text, div.text))
    tmp = datetime.now()
    output = dict(
           datenum = int((tmp - datetime(1970, 1, 1)).total_seconds()*1000),
           datestr = tmp.strftime("%Y-%m-%d %H:%M:%S"),
           information = ', '.join(out),
           list = out,
    )
    
    print 'Saving'
    with open(outfile,'a') as f:
        f.write('{datenum:d} : {datestr} : {information}\n'.format(**output))
    
    
    jsonfile = outfile.replace('.txt','.json')
    try:
        data = json.load(open(jsonfile, 'r'))
    except:
        data = []
    
    data.append(output)
    
    json.dump(data, open(jsonfile, 'w'), indent=2)
    