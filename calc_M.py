import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
from collections import Counter

#M STAT CALCULATION
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

def calculate_all_M(fp, outp):
    light_dump = []    
    counter =0
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