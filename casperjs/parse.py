#!/usr/bin/env python
import os
import sys
import matplotlib
matplotlib.use('agg')
import pylab
import numpy as np
from datetime import datetime
from pysurvey.plot import setup, dateticks

FILENAME = os.path.expanduser('~/data/bandwidth/archive.txt')
PLOT = ('plot' in sys.argv)
def parse():
    with open(FILENAME, 'r') as f:
        data = f.readlines()
    times = np.array([datetime.fromtimestamp(int(x.split(':')[0].strip())/1000.0) for x in data])
    values = np.array([int(x.split(':')[1].split('G')[0].strip()) for x in data])
    print 'Last Time: {} Value: {}'.format(datetime.now() - times[-1],values[-1])
    
    if PLOT:
        setup(figsize=(12,6), subplt=(1,2,1))
        pylab.plot(times,values)
        dateticks('%Y.%m.%d')
        
        setup(subplt=(1,2,2))
        pylab.plot(times[:-1],np.diff(values), 'sk')
        dateticks('%Y.%m.%d')
        
        pylab.savefig(os.path.expanduser('~/data/bandwidth/values.png'))

if __name__ == '__main__':
    parse()