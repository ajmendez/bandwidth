#!/usr/bin/env python
import os
import sys
import matplotlib
# matplotlib.use('agg')
import pylab
import numpy as np
from datetime import datetime
from pysurvey.plot import setup, dateticks
from matplotlib.dates import date2num

FILENAME = os.path.expanduser('~/data/bandwidth/archive.txt')
OUTFILE = os.path.expanduser('~/data/bandwidth/home.png')
PLOT = ('plot' in sys.argv)
def parse():
    with open(FILENAME, 'r') as f:
        data = f.readlines()
    times = np.array([datetime.fromtimestamp(int(x.split(':')[0].strip())/1000.0) for x in data])
    values = np.array([int(x.split(':')[1].split('G')[0].strip().replace('&lt;','')) for x in data])
    print 'Last Time: {} Value: {}'.format(datetime.now() - times[-1],values[-1])
    
    if PLOT:
        x = np.diff(values)
        ii = np.where(x > 0)
        setup(figsize=(8,8))
        
        setup(subplt=(2,2,1), subtitle='Monthly Integrated',
              ylabel='Cumulative GB per month',
              # ylog=True, yr=[1e-1, 2e3]
              )
        pylab.plot(times,values)
        pylab.plot(times[:-1][ii], x[ii], '.k', linewidth=0)
        dateticks('%m.%d')
        
        
        tmp = date2num(times[:-1][ii])
        setup(subplt=(2,2,2), subtitle='Daily Delta', xlabel='Date', ylabel='Daily GB',
              xr=[np.min(tmp), np.max(tmp)])
        days = np.ceil(np.max(tmp) - np.min(tmp))
        pylab.hist(tmp, bins=days, weights=x[ii],
                   alpha=0.75, linewidth=0.2, edgecolor='w')
        dateticks('%m.%d')
        
        
        setup(subplt=(2,2,3), subtitle='Week Delta', 
              xlabel='Day of the week', ylabel='GB / day of week',
              xtickv=np.arange(7)+0.5, xr=[0,7],
              xticknames=['sun','mon','tue','wed','thur','fri','sat']
              )
        tmp = (date2num(times[:-1]) % 7.0)
        pylab.hist(tmp[ii], bins=np.arange(0,8,0.25), weights=x[ii], 
                   alpha=0.75, linewidth=0.2, edgecolor='w')
        
        
        setup(subplt=(2,2,4), subtitle='Hour Delta',
              xlabel='Hour of the Day', ylabel='GB / hour of day',
              xr=[0,24],)
        tmp = (date2num(times[:-1]) % 1)*24.0
        pylab.hist(tmp[ii], bins=np.arange(0,25,1), weights=x[ii],
                   alpha=0.75, linewidth=0.2, edgecolor='w')
        # pylab.plot(tmp, np.diff(values), 'sk')
        # dateticks('%Y.%m.%d')
        
        
        
        
        
        pylab.tight_layout()
        # pylab.show()
        pylab.savefig(OUTFILE)

if __name__ == '__main__':
    from pysurvey.util import setup_stop
    setup_stop()
    parse()