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