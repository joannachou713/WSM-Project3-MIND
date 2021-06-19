'''
可改參數：
1. 讀取檔案
2. 選取的 threshold

選擇 -d 可以算各 score 的資訊
'''
import os
import pandas as pd
import sys, getopt

def inlinksGenerator(scoretype = 'tfidf', threshold = 77, describe = False, save = False):
    '''
    Check score descriptions
    '''    
    if describe:
        data = pd.read_table(f'newsinfo/MIND_{scoretype}_TOP100.txt',header=None,sep=' ',index_col=0)
        data['0'] = data.index
        data = data.reset_index()
        print(data.describe())    

    '''
    read filter
    '''
    print(scoretype, threshold, describe)
    scoretype = scoretype.upper()
    if scoretype=='BM25' and threshold==77 : threshold = 17

    result_dict = {}
    with open('newslist.txt') as newslist:
        newslist = list(newslist)
        for each in newslist:
            result_dict[each[:-6]] = []
        
    with open(f'newsinfo/MIND_{scoretype}_TOP100.txt') as tfidf:
        relations = tfidf.read().split('\n')
        for relation in relations:
            r_list = relation.split(' ')
            if float(r_list[2]) > threshold:
                result_dict[r_list[0]].append(r_list[1])

    '''
    save result txt
    '''
    if save:
        result_str = ''
        for key in result_dict.keys():
            result_str+=f'{key} {" ".join(result_dict[key])}\n'
        f = open(f"{scoretype}_inlink.txt", "w") 
        f.write(result_str) 
        f.close() 

    return result_dict