#!/usr/bin/env python
import matplotlib
matplotlib.use('agg')

import ast
import pylab
import numpy as np
from datetime import datetime
from matplotlib.dates import num2date, date2num


dtype = [
    ('date',     np.float64),
    ('upload',   np.float32),
    ('download', np.float32),
]

B2GB = 1073741824.0
filename = '/home/ajmendez/data/tplink.txt'


with open(filename, 'r') as f:
    lines = f.readlines()
    output = np.zeros(len(lines), dtype=dtype)
    for i,line in enumerate(lines):
        try:
            date,datestr,datastr = line.split('|')
            # print date, datestr,
            date = date2num(datetime.fromtimestamp(int(date.strip())))
            # print date, i
            data = ast.literal_eval(datastr.strip())
        except Exception as e:
            # print e
            continue
        output['date'][i] = date
        output['upload'][i] = data['wan_up_bytes']/B2GB
        output['download'][i] = data['wan_down_bytes']/B2GB
        # break

pylab.clf()
ii = np.where(output['date'] > 0)

pylab.title('Now: {:%m/%d %H:%M:%S}; Last: {:%m/%d %H:%M:%S}'.format(datetime.now(), num2date(output['date'][ii][-1])))

x = output['date'][ii]
x -= np.min(x)
u = np.diff(output['upload'][ii]) / np.diff(x)
d = np.diff(output['download'][ii]) / np.diff(x)


pylab.xlabel('Number of Days since Nov 4th')
pylab.ylabel('Gb / Day')
pylab.bar(left=x[1:][d>0], width=np.diff(x)[d>0],
          height=d[d>0], label='Download', alpha=0.7, lw=0, color='g')
pylab.bar(left=x[1:][u>0], width=np.diff(x)[u>0],
          height=u[u>0], label='Upload', alpha=0.7, lw=0, color='b')
pylab.legend()
pylab.tight_layout()
pylab.savefig('/home/ajmendez/data/tp_plot.png')
