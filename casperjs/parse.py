#!/usr/bin/env python
import os
import sys
import matplotlib
matplotlib.use('agg')
import pylab
from datetime import datetime
from pysurvey.plot import setup, dateticks

FILENAME = os.path.expanduser('~/data/bandwidth/archive.txt')
PLOT = ('plot' in sys.argv)
def parse():
    with open(FILENAME, 'r') as f:
        data = f.readlines()
    times = [datetime.fromtimestamp(int(x.split(':')[0].strip())/1000.0) for x in data]
    values = [int(x.split(':')[1].split('G')[0].strip()) for x in data]
    print 'Last Time: {} Value: {}'.format(datetime.now() - times[-1],values[-1])
    
    if PLOT:
        setup(figsize=(6,6))
        pylab.plot(times,values)
        dateticks('%Y.%M.%d')
        pylab.savefig('values.png')
    # for t,v in zip(times,values): print t,v

if __name__ == '__main__':
    parse()