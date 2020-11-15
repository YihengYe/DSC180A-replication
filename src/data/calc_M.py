import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
from collections import Counter

# M STAT CALCULATION: single article
def calculate_M(title, edits):
    edits.reverse()
    
    #cannot have edit war with 2 edits
    if len(edits) <= 2:
        return 0
    
    #cannot have edit war with less than 2 reverts
    try:
        num_reverts = sum([int(x[1]) for x in edits])
        if num_reverts < 2:
            return 0
    except:
        pass # bad data
    
    #M STAT: find revert pairs
    revert_pairs = []

    for lst in edits:
        if len(lst) < 4: # skip bad data
            continue
        
        if lst[1]=='1':  # is a revert
            user_one = lst[3]
            org_idx = int(lst[2])-1
            try:
                user_two = edits[org_idx][3]
            except:
                continue
            
            # exclude self revert
            if user_one == user_two:
                continue
            
            if (user_one, user_two) not in revert_pairs:
                revert_pairs.append((user_one, user_two))

    #M STAT: find mutual reverts
    mutual_rev_users = []
    mutual_rev_pairs = []
    for pair in revert_pairs:
        one = pair[0]
        two = pair[1]

        #mutual revert found
        if (two, one) in revert_pairs:
            mutual_rev_pairs.append((one, two))
            mutual_rev_users.append(two)
            mutual_rev_users.append(one)

    #remove duplicates, calculate num
    E = len(list(set(mutual_rev_users)))

    if E == 0:
        return 0
    
    #get num edits per user
    users = [x[3] for x in edits if len(x) == 4]
    user_edits = dict((x,users.count(x)) for x in set(users))
    
    #calculate M
    M = 0
    
    for pair in list(set(mutual_rev_pairs)):
        one = pair[0]
        two = pair[1]
        if user_edits[one] < user_edits[two]:
            N = user_edits[one]
        else:
            N = user_edits[two]

        M += N
    
    M *= E
    return M

# M STAT CALCULATION: entire light dump
def calculate_all_M(fp, outp):
    light_dump = []    
    counter =0
    outdir='data/M_calc'
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    with open(fp, encoding = 'utf8') as file:
        title = ''
        for line in file:

            #line is title
            if line[0] != "^": 
                if title != '':
                    #write previous M to file
                    with open(outp, 'a') as f:
                        M = calculate_M(title, light_dump)
                        f.write(title + ', ' + str(M) + '\n')

                    #reset var, continue reading
                    light_dump = []

                title = line.strip()

            #line is edit
            if line[0] == '^': 
                row = line[4:-1].split(' ')
                light_dump.append(row)

# EDA on M-stats
def generate_M_results(in_fp, outfp):
    
    # TOP 10 
    outp_top10 = outfp[0]
    with open(in_fp, 'rb') as file:
        data = []
        for line in file:
            try:
                line = line.decode()
                title, M = line.replace("\n", "").split(", ")
                data.append([title, int(M)])
            except:
                continue

    df = pd.DataFrame(data, columns = ['title', 'M'])
    df_top10 = df.sort_values('M', ascending = False).reset_index(drop = True).head(10)
    df_top10.to_csv(outp_top10, index = False)
    
    # M RATIO
    outp_ratio = outfp[1]
    ratio = [['M > 0', df[df.M > 0].count().iloc[0], df[df.M > 0].count().iloc[0] / len(df.M)] ]
    ratio.append(['M = 0', df[df.M == 0].count().iloc[0], df[df.M == 0].count().iloc[0] / len(df.M)])
    ratio = pd.DataFrame(data = ratio, columns = ['article M', 'frequency', 'proportion'])
    ratio.to_csv(outp_ratio, index = False)
    
    # Histogram
    outp_hist = outfp[2]
    fig = df[df.M > 0].plot.hist(bins = 50).get_figure()
    fig.savefig(outp_hist)

    # Quantiles
    outp_quant = outfp[3]

    quant = df[df.M>0].quantile([0,0.25,0.5,0.75,0.9,0.99,0.995,1])
    quant.to_csv(outp_quant)
    