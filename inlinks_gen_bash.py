'''
可改參數：
1. 讀取檔案
2. 選取的 threshold
選擇 -d 就只會算各 score 的資訊，不會轉成 inlink 格式
'''
import os
import pandas as pd
import sys, getopt

def main(argv):
    '''
    default params
    '''
    scoretype = 'tfidf'
    threshold = 77
    describe = False

    '''
    parse args
    '''
    try:
        opts, args = getopt.getopt(argv,"s:t:d",["scoretype=","threshold=", "describe="])
    except getopt.GetoptError:
        print('python3 inlinks_gen_bash.py [-s <scoretype(tfidf/bm25)> -t <threshold(recommend 77 / 17)>] or [-d]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python3 inlinks_gen_bash.py [-s <scoretype(tfidf/bm25)> -t <threshold(recommend 77 / 17)>] or [-d]')
            sys.exit()
        elif opt in ("-s", "--scoretype"):
            scoretype = arg
        elif opt in ('-t', '--threshold'):
            threshold = float(arg)
        elif opt in ('-d', '--describe'):
            describe = True

    '''
    Check score descriptions
    '''    
    if describe:
        data = pd.read_table(f'newsinfo/MIND_{scoretype}_TOP100.txt',header=None,sep=' ',index_col=0)
        data['0'] = data.index
        data = data.reset_index()
        print(data.describe())
        return
    

    '''
    read filter
    '''
    print(scoretype, threshold, describe)
    scoretype = scoretype.upper()
    if scoretype=='BM25' and threshold==77 : threshold = 17

    result_dict = {}
    for filename in os.listdir('MINDnews'):
        result_dict[filename[:-5]] = []

    with open(f'newsinfo/MIND_{scoretype}_TOP100.txt') as tfidf:
        relations = tfidf.read().split('\n')
        for relation in relations:
            r_list = relation.split(' ')
            if float(r_list[2]) > threshold:
                result_dict[r_list[0]].append(r_list[1])

    '''
    save result txt
    '''
    result_str = ''
    for key in result_dict.keys():
        result_str+=f'{key} {" ".join(result_dict[key])}\n'
    f = open(f"{scoretype}_inlinks.txt", "w") 
    f.write(result_str) 
    f.close() 



if __name__ == '__main__':
    main(sys.argv[1:])