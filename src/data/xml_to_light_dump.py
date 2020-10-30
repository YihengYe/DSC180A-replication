import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import zipfile
import re

def soupify_xml(fp):
    '''
    Processes xml data using beautiful soup and
    returns list of data for each page
    
    fp: file path of xml file
    '''
    content = []
    with open(fp, encoding = 'utf8') as file:

        content = file.readlines()
        content = "".join(content)
        soup = BeautifulSoup(content, "xml")
        
    pages = soup.findAll("page")
    return pages


def xml_to_df(pages):
    '''
    Converts soupified xml data for Wiki pages 
    into dataframe
    
    pages: list of xml data for each page
    '''
    data = {}
    for page in pages:
        title = page.title.text
        revisions = page.findAll("revision")

        for revision in revisions:
            r_id = revision.id.text 
            time = revision.timestamp.text
            try:
                username = revision.contributor.username.text
            except: 
                username = revision.contributor.ip.text
            text = revision.format.next_sibling.next_sibling.text
            if title in data:
                data[title].append([title, r_id, time, username, text])
            else:
                data[title] = [[title, r_id, time, username, text]]
    
    dframes = []
    for page in data:

        df = pd.DataFrame(data[page], columns = ['title', 'id', 'time', 'username', 'text'])

        hist = [] #history of text
        version = [] #edit version
        username = []
        revert = [] #0 or 1
        curr = 1 #to keep track of version

        for idx, row in df.iterrows():
            if row.text not in hist: # not a revert
                hist.append(row.text)
                version.append(curr)
                username.append(row.username)
                revert.append('0')
                curr += 1
            else: #is revert
                temp = hist.index(row.text)
                version.append(version[temp])
                username.append(row.username)

                #if self revert
                if row.username == username[version[temp]]:
                    revert.append('0')
                else:
                    revert.append('1')


        df['version'] = version
        df['revert'] = revert
        dframes.append(df)

    return dframes

def xml_to_light_dump(dframes, outpath):
    '''
    Given a list of cleaned dataframes from xml data,
    produces light dump file into data/raw
    '''
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    light_dump = ''
    for df in dframes:
        title = df.title[0]
        light_dump = light_dump + title + '\n'
        for idx, row in df.iterrows():
            line = '^^^_' + row.time + ' ' + row.revert + ' ' + str(row.version) + ' ' + row.username
            light_dump = light_dump + line + '\n'
    outfile = os.path.join(outpath, 'light_dump.txt')
    with open(outfile, 'w') as f:
        f.write(light_dump)
    repo = 'XML Converted to light dump at ' + outfile
    print(repo)
    
    return