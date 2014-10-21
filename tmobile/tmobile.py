#!/usr/bin/env python
import os
import time
from splinter import Browser
# from pymendez import auth
# from pysurvey.util import setup_stop
# setup_stop()

address = 'https://my.t-mobile.com/login/Default.aspx'
outfile = os.path.expanduser('~/data/bandwidth/tmobile_splinter.txt')


with open(os.path.expanduser('~/.limited/tmobile.auth'), 'r') as f:
    user,pw = f.read().strip().split(' ')
# user,pw = auth('tmobile',['username','password'])

tmp = dict(
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36"
)

# 
with Browser('chrome', **tmp) as browser:
    browser.visit(address)
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
        out.append('{} {}'.format(desc.text, div.text.splitlines()[0]))
    
    tmp = datetime.now()
    output = dict(
           datenum = int((tmp - datetime(1970, 1, 1)).total_seconds()*1000),
           datestr = tmp.strftime("%Y-%m-%d %H:%M:%S"),
           information = ', '.join(out),
    )
    
    
    with open(outfile,'a') as f:
        f.write('{datenum:d} : {datestr} : {information}\n'.format(**output))
    
    # raise ValueError()
    
    
    # time.sleep(1200)
    


#
#
# browser = Browser()
# browser.visit('http://google.com')
# browser.fill('q', 'splinter - python acceptance testing for web applications')
# browser.find_by_name('btnG').click()
#
# if browser.is_text_present('splinter.cobrateam.info'):
#     print "Yes, the official website was found!"
# else:
#     print "No, it wasn't found... We need to improve our SEO techniques"
#
# browser.quit()