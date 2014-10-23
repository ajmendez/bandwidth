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
              ylog=True, ylabel='Number', yr=[1e-1, 2e3])
        pylab.plot(times,values)
        pylab.plot(times[:-1][ii], x[ii], '.k', linewidth=0)
        dateticks('%m.%d')
        
        setup(subplt=(2,2,3), subtitle='by week')
        tmp = (date2num(times[:-1]) % 7)
        pylab.hist(tmp, bins=np.arange(0,7,1), alpha=0.75, linewidth=0)
        
        
        setup(subplt=(2,2,2), xticks=True, subtitle='By hour of the day')
        tmp = (date2num(times[:-1]) % 1)*24.0
        pylab.hist(tmp[ii], bins=np.arange(0,25,1), weights=x[ii],
                   alpha=0.75, linewidth=0.1, edgecolor='w')
        # pylab.plot(tmp, np.diff(values), 'sk')
        # dateticks('%Y.%m.%d')
        
        
        
        setup(subplt=(2,2,4), subtitle='By Day')
        days = np.ceil(np.max(date2num(times[:-1][ii])) - np.min(date2num(times[:-1][ii])))
        pylab.hist(date2num(times[:-1][ii]), bins=days, weights=x[ii],
                   alpha=0.75, linewidth=0)
        dateticks('%m.%d')
        pylab.tight_layout()
        pylab.show()
        pylab.savefig(os.path.expanduser('~/data/bandwidth/values.png'))

if __name__ == '__main__':
    from pysurvey.util import setup_stop
    setup_stop()
    parse()