#!/usr/bin/env python

import splinter
from bs4 import BeautifulSoup


def niceint(string):
    try:
        return int(string)
    except:
        return string


user, pw = open('/home/ajmendez/.limited/tp').readline().strip().split(',')

byte_names = ['wan_down_bytes', 'wan_up_bytes']
packet_names =  ['wan_down_packets', 'wan_up_packets']
data_names = ['total_packets', 'total_bytes', 'current_packets', 'current_bytes', 'icmp_tx', 'udp_tx', 'syn_tx']

browser_name = 'firefox'
browser_name = 'phantomjs'
out = {}
with splinter.Browser(browser_name) as b:
    b.visit('http://{user}:{pw}@192.168.0.1/'.format(**locals()))
    with b.get_iframe('mainFrame') as w:
        soup = BeautifulSoup(w.html)
    tmp = soup.find(id='t_byt').parent
    for name, item in zip(byte_names,tmp.findAll('td')[1:]):
        out[name] = niceint(item.text)
    tmp = soup.find(id='t_pcks').parent
    for name, item in zip(packet_names,tmp.findAll('td')[1:]):
        out[name] = niceint(item.text)
    out['uptime'] = soup.find(id='activeTime').text
    
    
    with b.get_iframe('bottomLeftFrame') as w:
        w.click_link_by_text('System Tools')
        w.click_link_by_text('- Statistics')
    
    with b.get_iframe('mainFrame') as w:
        b.select('Num_per_page','100')
        w.find_by_name('Refresh').first.click()
        soup = BeautifulSoup(w.html)
    
    
    for i, item in enumerate(soup.findAll('td', {'class':'ListM'})):
        if '192.168' not in item.text:
            continue
        computer = dict(
            ip = item.next,
            mac = item.next.next.next,
        )
        measures = item.parent.findAll('td', {'class':'Listm'})
        for name, data in zip(data_names, measures):
            computer[name] = niceint(data.text)
        out['computer_{}'.format(i)] = computer
    
print out
