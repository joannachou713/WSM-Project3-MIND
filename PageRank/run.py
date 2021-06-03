#
# https://github.com/garrettwang/PageRank
#

import sys,os
import time

start = time.time()
os.system("python3 PageRank.py > tfidf_result.txt")
end = time.time()
print("time elapsed" + str(end - start))
