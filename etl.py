'''
this is the file to contain all process data source code
'''

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


def extracter(raw, txtpath='data/unzipped'):
    '''
    this function take a file contains of .zip light_dump data and unzip them into txt

    raw: the string path to open

    '''
#     txtpath='data/unzipped'
    if not os.path.exists(txtpath):
        os.makedirs(txtpath)
    for zipname in os.listdir(raw):
        if zipname.endswith('.zip'):
            zipper=os.path.join(raw, zipname)
            the_zip=zipfile.ZipFile(zipper)
            for data in the_zip.namelist():
                datafile=os.path.join(txtpath, data)
                if not os.path.exists(datafile):
                    the_zip.extract(data, txtpath)
                    info='the data '+data+" has beeen store at "+txtpath
                    print(info)



    return

def ld_to_csv(txtpath, outpath):
    '''
    this code read txt files to csvs to store them at output path article by article

    txtpath: the path which store the txtfiles
    '''
#     outpath='data/csvs'
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for txtname in os.listdir(txtpath):
        txtroute=os.path.join(txtpath, txtname)
        filename=txtname.split('.')[0]
        filedir=os.path.join(outpath, filename)
        if not os.path.exists(filedir) and 'txt' in txtname:
            os.makedirs(filedir)
            with open(txtroute, 'r') as fh:
                table={'article':[],'time':[], 'revert':[], 'version':[], 'user':[]} #initialize the dataframe
                max_row=5000000
                rows=0
                count=0
                nowat=0
                exceed=False
                while True:
                    line=fh.readline()
                    content=line.strip()
                    if line.endswith('\n'):
                        content=line.strip()
                        if not '^^^' in content:
                            current=content
                            nowat +=1
                            if exceed:
                                count +=1
                                csvname=filename+'_'+str(count)+'.csv'
                                the_df=pd.DataFrame(table)
                                cvpath=os.path.join(filedir, csvname)
                                the_df.to_csv(cvpath, index=False)
                                print("creat 5-million-row table", count)
                                rows=0
                                table={'article':[],'time':[], 'revert':[], 'version':[], 'user':[]}
                                exceed=False

                        else:
                            if rows<max_row:
                                unit=content.split(' ')
                                time=unit[0][4:]
                                revert=unit[1]
                                version=unit[2]
                                user=unit[3]
                                table['time'].append(time)
                                table['revert'].append(revert)
                                table['version'].append(version)
                                table['user'].append(user)
                                table['article'].append(current)
                                rows +=1
                                nowat +=1
                            else:
                                unit=content.split(' ')
                                time=unit[0][4:]
                                revert=unit[1]
                                version=unit[2]
                                user=unit[3]
                                table['time'].append(time)
                                table['revert'].append(revert)
                                table['version'].append(version)
                                table['user'].append(user)
                                table['article'].append(current)
                                exceed=True
                                rows +=1
                                nowat +=1
                    else:
                        try:
                            unit=content.split(' ')
                            time=unit[0][4:]
                            revert=unit[1]
                            version=unit[2]
                            user=unit[3]
                            table['time'].append(time)
                            table['revert'].append(revert)
                            table['version'].append(version)
                            table['user'].append(user)
                            table['article'].append(current)
                            count +=1
                            csvname=filename+'_'+str(count)+'.csv'
                            the_df=pd.DataFrame(table)
                            cvpath=os.path.join(filedir, csvname)
                            the_df.to_csv(cvpath, index=False)
                            print("creat 5-million-row table", count)
                            rows=0
                            table={'article':[],'time':[], 'revert':[], 'version':[], 'user':[]}
                            exceed=False
                            break
                        except Exception as e:
                            count +=1
                            csvname=filename+'_'+str(count)+'.csv'
                            the_df=pd.DataFrame(table)
                            cvpath=os.path.join(filedir, csvname)
                            the_df.to_csv(cvpath, index=False)
                            print("creat 5-million-row table", count)
                            rows=0
                            table={'article':[],'time':[], 'revert':[], 'version':[], 'user':[]}
                            exceed=False
                            break
                            
                        
      

    return