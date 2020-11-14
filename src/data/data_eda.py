import pandas as pd
import matplotlib.pyplot as plt
import os
import gc
import requests
from bs4 import BeautifulSoup
import pandas as pd
import zipfile
import re
import time

def add_dicts(dict1, dict2):
    result={}
    if len(dict1.keys())==0:
        return dict2
    elif len(dict2.keys())==0:
        return dict1
    else:
        for key in dict1.keys():
            if key in dict2.keys():
                result[key]=dict1[key]+dict2[key]
            else:
                result[key]=dict1[key]
        for key2 in dict2.keys():
            if key2 not in result.keys():
                result[key2]=dict2[key2]
        return result
                
def get_csvs_route(road):
    result=[]
    for filename in os.listdir(road):
        fileroute=os.path.join(road,filename)
        result.append(fileroute)
    return result

def bots_raw_dict(road):
    total_freq={}
    revert_freq={}
    for csvname in os.listdir(road):
        csvroute=os.path.join(road, csvname)
        csvdict={}
        df=pd.read_csv(csvroute)
        df['user']=df['user'].str.lower()
        df['revert']=df['revert'].astype('int')
        dfrevert=df[df['revert']==1]
        bots=df[df['user'].str.contains('bot')]
        reverts=bots[bots['revert']==1]
        thef=bots['user'].value_counts().to_dict()
        ther=reverts['user'].value_counts().to_dict()
        total_freq=add_dicts(total_freq, thef)
        revert_freq=add_dicts(revert_freq, ther)
        print('finish dict csv', csvname, len(total_freq))
        del thef, ther
        del [[df, bots, reverts, dfrevert]]
        gc.collect()
        df=pd.DataFrame()
        bots=pd.DataFrame()
        reverts=pd.DataFrame()
        thef={}
        ther={}
        dfrevert=pd.DataFrame()
    return total_freq, revert_freq

def user_raw_dict(road):
    total_freq={}
    revert_freq={}
    for csvname in os.listdir(road):
        csvroute=os.path.join(road, csvname)
        csvdict={}
        df=pd.read_csv(csvroute)
        df['revert']=df['revert'].astype('int')
        reverts=df[df['revert']==1]
        thef=df['user'].value_counts().to_dict()
        ther=reverts['user'].value_counts().to_dict()
        total_freq=add_dicts(total_freq, thef)
        revert_freq=add_dicts(revert_freq, ther)
        print('finish dict csv', csvname, len(total_freq))
        del thef, ther
        del [[df, reverts]]
        gc.collect()
        df=pd.DataFrame()
        reverts=pd.DataFrame()
        thef={}
        ther={}
    return total_freq, revert_freq

def article_raw_dict(road):
    total_freq={}
    revert_freq={}
    for csvname in os.listdir(road):
        csvroute=os.path.join(road, csvname)
        csvdict={}
        df=pd.read_csv(csvroute)
        df['revert']=df['revert'].astype('int')
        reverts=df[df['revert']==1]
        thef=df['article'].value_counts().to_dict()
        ther=reverts['article'].value_counts().to_dict()
        total_freq=add_dicts(total_freq, thef)
        revert_freq=add_dicts(revert_freq, ther)
        print('finish dict csv', csvname, len(total_freq))
        del thef, ther
        del [[df, reverts]]
        gc.collect()
        df=pd.DataFrame()
        reverts=pd.DataFrame()
        thef={}
        ther={}
    return total_freq, revert_freq

def day_raw_dict(road):
    total_freq={}
    revert_freq={}
    for csvname in os.listdir(road):
        csvroute=os.path.join(road, csvname)
        csvdict={}
        df=pd.read_csv(csvroute)
        df['revert']=df['revert'].astype('int')
        df['time']=pd.to_datetime(df['time'])
        df['time']=df['time'].dt.floor('D')
        reverts=df[df['revert']==1]
        thef=df['time'].value_counts().to_dict()
        ther=reverts['time'].value_counts().to_dict()
        total_freq=add_dicts(total_freq, thef)
        revert_freq=add_dicts(revert_freq, ther)
        print('finish dict csv', csvname, len(total_freq))
        del thef, ther
        del [[df, reverts]]
        gc.collect()
        df=pd.DataFrame()
        reverts=pd.DataFrame()
        thef={}
        ther={}
    return total_freq, revert_freq

