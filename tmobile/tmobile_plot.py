#!/usr/bin/env python
import os
import json
import pylab
import numpy as np
from datetime import datetime
from matplotlib.dates import date2num
from pysurvey.plot import setup, dateticks



FILENAME = os.path.expanduser('~/data/bandwidth/tmobile_splinter.json')
OUTPLOT = os.path.expanduser('~/data/bandwidth/mobile.png')

def plot_tmobile():
    print 'building plot: ',
    data = json.load(open(FILENAME,'r'))
    print len(data)
    dates = [datetime.fromtimestamp(x['datenum']/1000)
             for x in data]
    mb = [float(x['list'][1].split()[1]) 
          for x in data]
    
    
    setup(figsize=(8,8))
    
    setup(subplt=(2,2,1), subtitle='MB / Month',
          xlabel='Date', ylabel='Cumulative MB per month')
    # pylab.plot(dates, mb)
    pylab.fill_between(dates, np.zeros(len(mb)), mb)
    dateticks('%y-%m-%d')
    
    setup(subplt=(2,2,2), subtitle='MB',
          xlabel='Date', ylabel='MB per 6hr')
    x = np.array(dates[:-1])
    y = np.diff(mb)
    ii = np.where(y >= 0)
    x,y = x[ii],y[ii]
    # pylab.plot(x,y)
    pylab.fill_between(x, np.zeros(len(y)), y)
    dateticks('%y-%m-%d')
    
    setup(subplt=(2,2,3), subtitle='MB / Hour of Day',
          xlabel='Hour of Day', xr=[0,24],
          ylabel='Cumulative MB per Hour')
    hourofday = (date2num(x) % 1.0)*24.0
    bins = np.arange(0,24,1)
    pylab.hist(hourofday, bins, weights=y)
    
    setup(subplt=(2,2,4), subtitle='MB / Day of Week',
          xlabel='Day of Week', ylabel='Cumulative MB per Day',
          xtickv=np.arange(7)+0.5, xr=[0,7],
          xticknames=['sun','mon','tue','wed','thur','fri','sat'])
    dayofweek = date2num(x) % 7.0
    bins = np.arange(8)
    pylab.hist(dayofweek, bins, weights=y)
    
    pylab.tight_layout()
    pylab.savefig(OUTPLOT)
    
    # pylab.show()


if __name__ == '__main__':
    plot_tmobile()
