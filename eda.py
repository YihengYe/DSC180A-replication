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
    '''
    helper function to add two dict together
    '''
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
    '''
    get all filles with csvs in it
    '''
    result=[]
    for filename in os.listdir(road):
        fileroute=os.path.join(road,filename)
        result.append(fileroute)
    return result

def bots_raw_dict(road):
    '''
    create bots dict
    '''
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
    '''
    create_user_dict
    '''
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
    '''
    create_article_dict
    '''
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
    '''
    create daily dict
    '''
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

def generate_result(road, content):
    '''
    generate_result
    '''
    if content=='bots':
        edit,revert=bots_raw_dict(road)
    elif content=='day':
        edit,revert=day_raw_dict(road)
    elif content=='article':
        edit,revert=article_raw_dict(road)
    elif content=='user':
        edit,revert=user_raw_dict(road)
    else:
        print('Not Defined!')
    column1=content+'_edit'
    column2=content+'_revert'
    column3=content+'_revert_edit_ratio'
    edit_series=pd.Series(edit)
    revert_series=pd.Series(revert)
    combined_df=pd.concat([edit_series,revert_series], axis=1)
    combined_df.columns=[column1,column2]
    combined_df[column3]=combined_df[column2]/combined_df[column1]
    combined_df=combined_df.fillna(0)
    routename=os.path.basename(os.path.normpath(road))
    output_path='result/eda/'+routename
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # make description csv
    result1=column1+"_describe.csv"
    result2=column2+"_describe.csv"
    result3=column3+"_describe.csv"
    outpath1=os.path.join(output_path, result1)
    outpath2=os.path.join(output_path, result2)
    outpath3=os.path.join(output_path, result3)
    combined_df[column1].describe().to_csv(outpath1, index=False)
    combined_df[column2].describe().to_csv(outpath2, index=False)
    combined_df[column3].describe().to_csv(outpath3, index=False)
    #draw pictures,edit
    plt.figure()
    plt.plot(combined_df[column1])
    plt.xlabel(content)
    plt.ylabel('edit_frequency')
    plt.title(column1)
    pig=column1+"_plot.png"
    outpath4=os.path.join(output_path, pig)
    plt.savefig(outpath4)
    plt.close()
    #draw pictures,revert
    plt.figure()
    plt.plot(combined_df[column2])
    plt.xlabel(content)
    plt.ylabel('revert_frequency')
    plt.title(column2)
    pig=column2+"_plot.png"
    outpath5=os.path.join(output_path, pig)
    plt.savefig(outpath5)
    plt.close()

    #draw pictures,revert/edit ratio
    plt.figure()
    plt.hist(combined_df[column3])
    plt.xlabel(content)
    plt.ylabel('ratio_frequency')
    plt.title(column3)
    pig=column3+"_histogram.png"
    outpath6=os.path.join(output_path, pig)
    plt.savefig(outpath6)
    plt.close()
    
    return

