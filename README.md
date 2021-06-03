# WSM-Project3-MIND
## Page Rank Algorithm on MIND news datasets
### File Trees
```
├── MINDlarge_test
├── MINDlarge_train
├── MINDnews              # contains each news' html file
├── newsinfo              # contains each news' top 100 news based on TFIDF and BM25
├── PageRank
│   ├── PageRank.py
│   ├── run.py            # PageRank.py's command line caller
│   └── tfidfResult.py
├── .gitignore
├── links_gen_bash.py     # Generate news relations to count page rank (can run on terminal)
├── linksGenerator.py     # Generate news relations to count page rank (used in other .py file)
├── preprocessing.py      # no use, to be deleted
├── run_pagerank.py       # PageRank's main 
└── tfidf.py              # to be deleted
```

### How to run these functions
1. `run_pagerank.py`:
    ```
    python3 run_pagerank.py -s <score_type> -t <threshold> -c <count>
    ```
    If no parameter is given, then it will run in default mode
    ```
    score_type = tfidf
    threshold = 0
    count = 50
    ```
2. `links_gen_bash.py`
    ```
    python3 inlinks_gen_bash.py [-s <scoretype(tfidf/bm25)> -t <threshold(recommend 77 / 17)>] or [-d]
    ```
    If `-d` is chosen, then the program will only show the description/summary of chosen scores.
    This function requires `/MINDnews` which contains each news' `html` file, and `/newsinfo` which contains top 100 related news according to each news counted in TFIDF/BM25

  
  
  
  
  
  
