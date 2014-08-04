#!/usr/bin/env python
import os
import pylab
import numpy as np
from datetime import datetime, timedelta
from calendar import monthrange, day_abbr
from pysurvey.plot import setup, dateticks
from matplotlib.dates import date2num, num2date



DATAFILE = '~/dev/network/traffic2'


with open(os.path.expanduser(DATAFILE),'r') as f:
    data = f.readlines()

out = {}
for line in data:
    if line.startswith('#'):
        continue
    prefix,ud = line.split('=')
    days = ud.strip().split(' ')
    date = datetime.strptime(prefix,'traff-%m-%Y')
    
    if len(days) == monthrange(date.year, date.month)[1]+2:
        days = days[:-2]
    
    if len(days) > monthrange(date.year, date.month)[1]:
        print "Number of days"
        print date, len(days), monthrange(date.year, date.month)[1]
        print days
        raise ValueError()
    
    for i,day in enumerate(days):
        key = date2num(date + timedelta(days=i))
        down,up = map(int, day.replace('[','').replace(']','').split(':'))
        if key in out:
            if up > out[key]['up']:
                out[key]['up'] = up
            if down > out[key]['down']:
                out[key]['down'] = down
            
        else:
            out[key] = dict(up=up, down=down)

dates = sorted([key for key in out])

up   = np.array([out[key]['up'] for key in dates])
down = np.array([out[key]['down'] for key in dates])
percent = float(len([1 for k in dates if (out[k]['down']>0)]))/(max(dates)-min(dates))
totalup = np.sum(up)/1000/1000/percent
totaldown = np.sum(down)/1000/1000/percent
print 'up: {}, down: {}, percent: {}'.format(totalup, totaldown, percent)




logup   = np.log10(up)
logdown = np.log10(down)



xr = date2num([datetime(2009,01,01), datetime(2015,01,01)])
xtickv = np.linspace(*xr,num=7)
setup(figsize=(8,12), subplt=(2,1,1),
      title='Gateway02 Percent Logged: {:0.0f}%'.format(percent*100),
      subtitle='Blue: Uploaded Total:{:0.1f}TB\nGreen: Downloaded Total: {:0.1f}TB'.format(totalup, totaldown),
      xr=xr, xtickv=xtickv, xlabel='Date',
      yr=[-5.5,5.5], ylabel='Log Megabytes Transferred per Day',
      )
pylab.bar(dates, logup,    width=1, alpha=0.7, color='b', linewidth=0)
pylab.bar(dates, -logdown, width=1, alpha=0.7, color='g', linewidth=0)
dateticks('%Y-%m-%d')



upweek = np.zeros(7)
downweek = np.zeros(7)
std = { t:{i:[] for i in range(7)} 
              for t in ['up','down']}
print std
start = date2num(datetime(2008,12,29)) # Monday
n = np.zeros(7)
for key,u,d in zip(dates,up,down):
    if u <= 0 and d <= 0:
        continue
    # if d >= 30000:
    #     continue
    i = (key-start) % 7
    upweek[i] += u
    downweek[i] += d
    std['up'][i].append(u)
    std['down'][i].append(d)
    n[i] += 1
    if i == 2:
        print d, num2date(key)
upstd   = np.array([np.std(std['up'][i]) for i in range(7)])/np.sqrt(n)
downstd = np.array([np.std(std['down'][i]) for i in range(7)])/np.sqrt(n)

print upweek, upstd/1000.0


setup(subplt=(2,1,2),
      subtitle='Blue: Upload\nGreen:Download',
      title='Average Week',
      xr=[0,7], xtickv=np.arange(7)+0.5, xticknames=list(day_abbr),
      # hspace=0.25,
      ylabel='Avgerage GB per day'
      )
index = np.arange(7)+0.5
pylab.bar(index-0.25, upweek/n/1000.0, width=0.25, color='b', alpha=0.7, linewidth=0)
pylab.bar(index+0, downweek/n/1000.0,  width=0.25, color='g', alpha=0.7, linewidth=0)
pylab.errorbar(index-0.125, upweek/n/1000.0, upstd/1000.0,      fmt=',b', alpha=0.7, linewidth=2)
pylab.errorbar(index+0.125, downweek/n/1000.0,  downstd/1000.0, fmt=',g', alpha=0.7, linewidth=2)
setup(embiggeny=[0,0.25])

pylab.tight_layout()

pylab.show()


# years = range(2009,2013)
# months = range(1,13)
#
# with open(os.path.expanduser(dataFile),'r') as f:
#     data = f.readlines()
#
# for year in years:
#     for month in months:
#         # find this line of traff
#         print "traff-%d-%d"%(year,month)
#
#         # parse the upload:download for each day
#         # store it in some array
#
# # go through array and print it in a nice csv format for google spreadsheet
#
