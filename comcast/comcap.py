#! /usr/bin/env python
"""
This is a simple mechanize script that logs into Comcast, retrieves the usage
information, and prints it to stdout.

Requires mechanize.

Copyright (C) 2011 Jared Hobbs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import sys
import cookielib
from getpass import getpass
from netrc import netrc

import mechanize

LOGIN = 'https://login.comcast.net/login?continue=https://login.comcast.net/account'
USERS = 'https://customer.comcast.com/Secure/Users.aspx'
SERVICES = 'https://customer.comcast.com/Secure/MyServices/'
PRELOADER = 'https://customer.comcast.com/Secure/Preload.aspx?backTo=%2fSecure%2fUsers.aspx&preload=true'
PRELOADER = 'https://customer.comcast.com/Secure/Preload.aspx?backTo=%2fSecure%2fMyServices/?ajax=1&preload=true'
AJAX = 'https://customer.comcast.com/Secure/MyServices/?ajax=1'
EQUIPMENT = AJAX + '&control=Equipment'

def debug(t, v, tb):
    import traceback, pdb
    traceback.print_exception(t, v, tb)
    print
    pdb.pm()

sys.excepthook = debug

def getBrowser():
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_redirect(True)
    br.set_handle_equiv(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=5)
    br.add_handler(mechanize.HTTPSHandler())
    br.addheaders = [('User-agent',
                      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3'),]
    return br

def login(br):
    from pymendez import auth
    username, password = auth('comcast', ['username', 'password'])
    
    # try:
    #     n = netrc()
    #     username, account, password = n.authenticators('login.comcast.net')
    #     if None in (username, password):
    #         raise
    # except:
    #     username = raw_input('Username: ')
    #     password = getpass()
    br.open(LOGIN)
    br.select_form(name='signin')
    br.form['user'] = username
    br.form['passwd'] = password
    br.submit()
    try:
        br.select_form(name='signin')
        br.form['passwd'] = password
        br.submit()
    except:
        pass
    try:
        br.select_form(name='redir')
    except mechanize._mechanize.FormNotFoundError:
        raise Exception('Failed to login')
    br.submit()

def printBandwidthUsage(br):
    br.open(USERS)
    br.open(PRELOADER)
    br.open(SERVICES)
    br.open(AJAX, timeout=60.0)
    br.open(EQUIPMENT, timeout=60.0)
    response = br.response()
    soup = mechanize._beautifulsoup.BeautifulSoup(response.read())
    print soup.prettify()
    try:
        usagetext = soup.fetch('p')[-1].contents[0].split()[3]
        print usagetext
    except:
        raise Exception('Failed to find bandwidth usage.')

def main():
    br = getBrowser()
    login(br)
    printBandwidthUsage(br)

if __name__ == '__main__':
    main()