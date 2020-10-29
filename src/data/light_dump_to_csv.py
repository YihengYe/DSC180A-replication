import pandas as pd
import zipfile
import os
import re

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
        if not os.path.exists(filedir):  #use a file to store all articles in this wiki
            os.makedirs(filedir)
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
                        if exceed:
                            count +=1
                            csvname=filename+'_'+str(count)+'.csv'
                            the_df=pd.DataFrame(table)
                            cvpath=os.path.join(filedir, csvname)
                            the_df.to_csv(cvpath, index=False)
                            rows=0
                            table={'article':[],'time':[], 'revert':[], 'version':[], 'user':[]}
                            exceed=False

                    else:
                        if rows<max_row and nowat<maxline:
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
                        elif rows>=max_row and nowat<maxline:
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
                            count +=1
                            csvname=filename+'_'+str(count)+'.csv'
                            the_df=pd.DataFrame(table)
                            cvpath=os.path.join(filedir, csvname)
                            the_df.to_csv(cvpath, index=False)
                            rows=0
                            table={'article':[],'time':[], 'revert':[], 'version':[], 'user':[]}
                            exceed=False

          



    return