from __future__ import division, unicode_literals
import math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)



########################################################


def clean(s):
    s = s.replace(".","")
    s = s.replace(",","")
    s = s.replace(":","")
    s = s.replace(":","")
    s = s.replace("[","")
    s = s.replace("]","")
    s = s.replace(")","")
    s = s.replace("(","")
    s = s.replace("{","")
    s = s.replace("}","")
    s = s.replace("/","")
    s = s.replace("?","")
    s = s.replace("!","")
    s = s.replace("’","")
    s = s.replace("'","")
    s = s.replace('"',"")
    s = s.replace('”',"")
    return s

def getTitles(records,t):
    records = records.split(' ')
    titles = []
    if t == 'h':
        for record in records:
            r_temp = []
            for r in news[record]:
                r = clean(r)
                r_temp+=r.split(' ') 
            titles+=r_temp
    if t == 'c':
        for record in records:
            r_temp = []
            for r in news[record[:-2]]:
                r = clean(r)
                r_temp+=r.split(' ') 
            titles+=r_temp
    return ' '.join(titles)


# Main(?)
behaviors = open('MINDlarge_train/behaviors.tsv')
news = open('MINDlarge_train/news.tsv').read().split('\n')
news = { n.split('\t')[0]: n.split('\t')[1:5] for n in news }

# 要執行時在把 [:1000] 刪掉，會加這段是因為怕電腦跑不動
exp = behaviors.read()[:1000]
exp = exp.split('\n')
for record in exp:
    record = record.split('\t')
    hist_titles = getTitles(record[3],'h')
    can_titles = getTitles(record[4],'c')
    print(hist_titles)
    print(can_titles)

    document1 = tb(hist_titles)
    document2 = tb(can_titles)

    bloblist = [document1, document2]

    for i, blob in enumerate(bloblist):
        print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:3]:
            print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
    
    # ...count tfidf?
    # 要跑全部的 behavior 的話這個 break 也要刪掉
    break



