'''
this is the file to contain all process data source code
'''

import os
import requests
from bs4 import BeautifulSoup




def donwload_data(links, outpath):
    '''
    download data by list of links given

    links: a list of string links
    outpath: a string of output path
    '''
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for link in links:
        filename=link.split('/')[-1]
        outfile=os.path.join(outpath, filename)
        if not os.path.exists(outfile): #do not redunant download
            r=requests.get(link, outfile)
            with open(outfile, 'wb') as f:
                f.write(r.content)
        repo='Successfully download data from '+link+' at '+outfile
        print(repo)

    return