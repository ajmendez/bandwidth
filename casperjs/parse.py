#!/usr/bin/env python
import os
import sys
import matplotlib
matplotlib.use('agg')
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
    values = np.array([int(x.split(':')[1].split('G')[0].strip()) for x in data])
    print 'Last Time: {} Value: {}'.format(datetime.now() - times[-1],values[-1])
    
    if PLOT:
        setup(figsize=(8,8), subplt=(2,2,1))
        pylab.plot(times,values)
        dateticks('%Y.%m.%d')
        
        setup(subplt=(2,2,3))
        pylab.plot(times[:-1],np.diff(values), 'sk')
        dateticks('%Y.%m.%d')
        
        setup(subplt=(2,2,2))
        tmp = (date2num(times[:-1]) % 1)*24.0
        pylab.hist(tmp, bins=np.arange(0,25,2), weights=np.diff(values))
        # pylab.plot(tmp, np.diff(values), 'sk')
        # dateticks('%Y.%m.%d')
        
        pylab.savefig(os.path.expanduser('~/data/bandwidth/values.png'))

if __name__ == '__main__':
    from pysurvey.util import setup_stop
    setup_stop()
    parse()