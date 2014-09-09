#!/usr/bin/env python
'''Get the comcast usage for the day'''

import twill
import requests
from pymendez import auth



# username, password, eqs = auth('comcast', ['username','password','eqs'])
# webpage = 'https://customer.comcast.com/Secure/UsageMeterDetail.aspx?eqs={}'.format(eqs)

username, password = auth('comcast', ['username','password'])
webpage = 'https://customer.comcast.com/MyServices/Internet/?ajax=1'
# loginpage = 'https://login.comcast.net/login'

def getcookies(url, username=username, password=password):
    twill.commands.go(url)
    # twill.commands.formaction('1', loginpage)
    twill.commands.formclear('1')
    twill.commands.fv('1', 'user', username)
    twill.commands.fv('1', 'passwd', password)
    twill.commands.submit('1')
    browser = twill.commands.get_browser()
    return browser._session.cookies

def getpage(url, cookies):
    response = requests.get(url, cookies=cookies)
    print 'GB' in response.text
    print response.text


def comcast():
    cookies = getcookies(webpage)
    page = getpage(webpage, cookies)
    




if __name__ == '__main__':
    comcast()