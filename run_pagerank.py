import os
import pandas as pd
import sys, getopt

def main(argv):
    '''
    default params
    '''
    tfidf_threshold = 77
    bm25_threshold = 17
    inlinks = False

    '''
    parse args
    '''
    try:
        opts, args = getopt.getopt(argv,"t:b:i",["tfidf=","bm25=","inlinks="])
    except getopt.GetoptError:
        print('python3 run_pagerank.py -t <tfidf_threshold> -b <bm25_threshold>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python3 top100_inlink_generator.py -t <tfidf_threshold> -b <bm25_threshold>')
            sys.exit()
        elif opt in ("-t", "--tfidf"):
            tfidf_threshold = float(arg)
        elif opt in ('-b', '--bm25'):
            bm25_threshold = float(arg)
        elif opt in ('-i', '--inlinks'):
            inlinks = True
    
    if inlinks:
        os.system(f"python3 top100_inlink_generator.py -s tfidf -t {tfidf_threshold}")
        os.system(f"python3 top100_inlink_generator.py -s bm25 -t {bm25_threshold}")
    
    behaviors = open('MINDlarge_train/behaviors.tsv')


