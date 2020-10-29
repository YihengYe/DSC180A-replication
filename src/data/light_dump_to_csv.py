import pandas as pd
import zipfile
import os

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
    this code read txt files to a folder that contains csvs about each articles store in the txt file

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
            with open(txtroute, 'r') as fh:
                print('yes')

    return