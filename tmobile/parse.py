#!/usr/bin/env python
import os
import re
import matplotlib
matplotlib.use('agg')
from bs4 import BeautifulSoup
from datetime import datetime
from matplotlib import pyplot as plt
from pysurvey.plot import setup, dateticks


DIRNAME = os.path.expanduser('~/data/bandwidth')
FILENAME = DIRNAME + '/tmobile.txt'

OUTFILE = DIRNAME + '/tmobile_simple.txt'
OUTPLOT = DIRNAME + '/tmobile_plot.png'


def togb(x):
    out = float(x.split()[0])
    scale = dict(KB=1e-3, MB=1, GB=1e3)
    for k,v in scale.items():
        if k in x:
            return out*v

def getsoup(instring):
    soup = BeautifulSoup(instring)
    minute, data = [x.text for x in soup.findAll('span', {'class':'home-txt20'})]
    return int(minute), togb(data)




def parse():
    dates = []
    tmp = []
    out = []
    with open(FILENAME,'r') as infile:
        for line in infile.readlines():
            x = re.match('^([0-9]+) :(.+)', line)
            if x is None:
                tmp.append(line.strip())
            else:
                y = x.groups()
                dates.append(int(y[0]))
                if len(tmp) > 0:
                    data = getsoup(''.join(tmp))
                    out.append(data)
                    tmp = []
                else:
                    tmp.append(y[1])
        data = getsoup(''.join(tmp))
        out.append(data)
            # break

    dates = [datetime.fromtimestamp(int(d)/1000) for d in dates]
    minutes = [o[0] for o in out]
    megabytes = [o[1]for o in out]

    with open(OUTFILE, 'w') as outfile:
        fmt = '{0:} : {1[0]: 4d} Min {1[1]: 6.1f} MB\n'
        for d,o in zip(dates,out):
            outfile.write(fmt.format(d, o))
    
    
    print len(dates), len(minutes), len(megabytes)
    
    setup(figsize=(12,6), subplt=(1,2,1), xlabel='', ylabel='Minutes')
    plt.plot(dates, minutes)
    dateticks()
    
    setup(subplt=(1,2,2), xlabel='', ylabel='MB')
    plt.plot(dates, megabytes)
    dateticks()
    setup(wspace=0.3)
    plt.savefig(OUTPLOT, dpi=60)
    
    

if __name__ == '__main__':
    parse()