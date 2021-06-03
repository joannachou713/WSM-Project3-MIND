import functools
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

    '''
    parse args
    '''
    try:
        opts, args = getopt.getopt(argv,"s:t:c:",["score_type=","threshold=", "count="])
    except getopt.GetoptError:
        print('python3 run_pagerank.py -s <score_type> -t <threshold> -c <count>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python3 run_pagerank.py -s <score_type> -t <threshold> -c <count>')
            sys.exit()
        elif opt in ("-s", "--score_type"):
            scoretype = arg
        elif opt in ('-t', '--threshold'):
            threshold = float(arg)
        elif opt in ('-c', '--count'):
            count = float(arg)
    
    final_txt = open(f"{scoretype}_prediction.txt", "w") 
    
    behaviors = open('MINDlarge_test/behaviors.tsv')
    totalRank = tfidfResult.all_result[:100]
    imps = behaviors.read()
    imps = imps.split('\n')
    
    '''
    Generate inlink_dict
    '''
    inlinks_dict = inlinksGenerator.inlinksGenerator(scoretype,threshold, describe = False, save = False)

    for imp in imps[1486019:]:
        imp = imp.split('\t')
        imp_id = imp[0]
        print(imp_id)
        hist_list = imp[3].split(' ')
        can_list = imp[4].split(' ')

        if hist_list!=['']:
            '''
            get hists inlinks and put them in a string
            '''
            inlinks_imp_history = ''
            for hist in hist_list+can_list:
                hist_links = [link for link in inlinks_dict[hist] if link in can_list or link in hist_list]
                inlinks_imp_history += f'{hist} {" ".join(hist_links)}\n'
            # for can in can_list:
            #     can_links = [link for link in inlinks_dict[can] if link in can_list or link in hist_list]
            #     inlinks_imp_history += f'{can} {" ".join(can_links)}\n'
            
            # inlinks_imp_history = ''.join(list(map(lambda a: f'{a} {" ".join(list(filter(lambda x: x in (can_list+hist_list), inlinks_dict[a])))}\n', (hist_list+can_list))))
            
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

    
    final_txt.close() 

if __name__ == '__main__':
    main(sys.argv[1:])