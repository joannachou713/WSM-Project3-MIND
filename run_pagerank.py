import functools,time
import pandas as pd
import sys, getopt
import inlinksGenerator 
from PageRank import PageRank,tfidfResult

def main(argv):
    '''
    default params
    '''
    scoretype = 'tfidf'
    threshold = 0
    count = 50
    train = False

    '''
    parse args
    '''
    try:
        opts, args = getopt.getopt(argv,"s:t:c:r",["score_type=","threshold=", "count=", "train="])
    except getopt.GetoptError:
        print('python3 run_pagerank.py -s <score_type> -t <threshold> -c <count> [-r]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python3 run_pagerank.py -s <score_type> -t <threshold> -c <count> [-r]')
            sys.exit()
        elif opt in ("-s", "--score_type"):
            scoretype = arg
        elif opt in ('-t', '--threshold'):
            threshold = float(arg)
        elif opt in ('-c', '--count'):
            count = float(arg)
        elif opt in ('-r', '--train'):
            train = True
    
    final_txt = open(f"{scoretype}_prediction.txt", "w") 
    
    behaviors_path = 'MINDlarge_train/behaviors.tsv' if train else 'MINDlarge_test/behaviors.tsv'
    behaviors = open(behaviors_path)
    totalRank = tfidfResult.all_result
    imps = behaviors.read()
    imps = imps.split('\n')
    
    '''
    Generate inlink_dict
    '''
    inlinks_dict = inlinksGenerator.inlinksGenerator(scoretype,threshold, describe = False, save = False)

    start = time.time()
    for imp in imps:
        imp = imp.split('\t')
        imp_id = imp[0]
        hist_list = imp[3].split(' ')
        can_list = imp[4].split(' ')
        if train:
            can_list = [can[:-2] for can in can_list]


        if hist_list!=['']:
            '''
            get hists inlinks and put them in a string
            '''
            inlinks_imp_history = ''
            for hist in hist_list+can_list:
                hist_links = [link for link in inlinks_dict[hist] if link in can_list or link in hist_list]
                inlinks_imp_history += f'{hist} {" ".join(hist_links)}\n'
           
            f = open("temp_inlink.txt", "w") 
            f.write(inlinks_imp_history) 
            f.close() 

            pr_result = PageRank.main("temp_inlink.txt",count)
            sorted_news = [pr[1] for pr in pr_result if pr[1] in can_list]
        else:
            sorted_news = [pr[1] for pr in totalRank if pr[1] in can_list]

        final_result = [0]*len(can_list)
        for i, result in enumerate(sorted_news):
            final_result[can_list.index(result)] = i+1
        final_txt.write(f'{imp_id} {final_result}\n') 

    end = time.time()
    print(end-start)
    final_txt.close() 

if __name__ == '__main__':
    main(sys.argv[1:])