# import fileinput
#
# for line in fileinput.input():
#     pass

import os
import sys
import json
import dateutil.parser
from datetime import datetime
from bs4 import BeautifulSoup



def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
 
def object_hook(obj):
  if 'date' in obj:
    obj['date'] = dateutil.parser.parse(obj['date']) 
  return obj

class Data(object):
    '''The json dictionary container that holds the all of the song data.'''
    def __init__(self, filename, fcn=list):
        self.filename = os.path.expanduser(filename)
        self.fcn = fcn
    
    def __iter__(self):
        for item in self.data:
            yield item
    
    def insert(self, index, item):
      self.data.insert(index, item)
    
    def __enter__(self, *args, **kwargs):
        try:
            self.data = json.load(open(self.filename),
                                  object_hook=object_hook)
        except Exception as e:
            print e
            print ' Failed to load: {}'.format(self.filename)
            self.data = self.fcn()
        return self
    
    def __exit__(self, *args, **kwargs):
        json.dump(self.data, 
                  open(self.filename,'w'),
                  default=date_handler,
                  indent=2)




if __name__ == '__main__':
    data = sys.stdin.read()
    soup = BeautifulSoup(data)
    

    s = soup.find('div',{'class':'cui-usage-bar'})
    try:
        total = int(s.find('span').get('data-used'))
    except:
        total = -1
    try:
        string = s.find('span',{'class':'accessibly-hidden'}).text.strip()
    except:
        string = ""


    with Data('~/data/bandwidth/comcast.json') as output:
        tmp = dict(
            date = datetime.now(),
            total = total,
            string = string,
        )
        output.insert(-1, tmp)