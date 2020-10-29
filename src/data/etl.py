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
    data = []
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
            data.append([title, r_id, time, username, text])
    
    df = pd.DataFrame(data, 
                      columns = ['title', 'id', 'time', 
                                 'username', 'text'])

    return df



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


def extracter(raw):
    '''
    this function take a file contains of .zip light_dump data and unzip them into txt

    raw: the string path to open

    '''
    txtpath='data/unzipped'
    if not os.path.exists(txtpath):
        os.makedirs(txtpath)
    for zipname in os.listdir(raw):
        zipper=os.path.join(raw, zipname)
        the_zip=zipfile.ZipFile(zipper)
        for data in the_zip.namelist():
            datafile=os.path.join(txtpath, data)
            if not os.path.exists(datafile):
                the_zip.extract(data, txtpath)
                info='the data '+data+" has beeen store at "+txtpath
                print(info)



    return

def ld_to_csv(txtpath):
    '''
    this code read txt files to csvs to store them at output path article by article

    txtpath: the path which store the txtfiles
    '''
    outpath='data/csvs'
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for txtname in os.listdir(txtpath):
        txtroute=os.path.join(txtpath, txtname)
        filename=txtname.split('.')[0]
        filedir=os.path.join(outpath, filename)
        if not os.path.exists(filedir):
            os.makedirs(filedir)
            tables={}
            with open(txtroute, 'r') as fh:
                lines=fh.readlines()
                table={'article':[],'time':[], 'revert':[], 'version':[], 'user':[]} #initialize the dataframe
                max_row=100000
                rows=0
                count=0
                nowat=0
                maxline=len(lines)
                for line in lines:
                    content=line.strip()
                    if not '^^^' in content:
                        current=content
                        nowat +=1
                    else:
                        if rows<max_row and nowat<maxline:
                            unit=content.split(' ')
                            time=unit[0][3:]
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
                            count +=1
                            csvname=filename+'_'+str(count)+'.csv'
                            the_df=pd.DataFrame(table)
                            cvpath=os.path.join(filedir, csvname)
                            the_df.to_csv(cvpath, index=False)
                            rows=0
                            table={'article':[],'time':[], 'revert':[], 'version':[], 'user':[]}
                            unit=content.split(' ')
                            time=unit[0][3:]
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
    return