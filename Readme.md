mulanalyze.py
Calculate ratio of TP, FN, TN, FP due to threshold.
$ python3 mulanalyze.py [log dir] [high | low]
Ex)
$ python3 mulanalyze.py logs/origin/ high > origin_high.csv
$ python3 mulanalyze.py logs/origin/ low > origin_high.csv
$ python3 mulanalyze.py logs/comb_dude/ low > dude_high.csv

condprob.py
Calculate conditional probability due to confidence from littel model
$ python3 condprob.py [log dir] [interval] [threshold of big model]
Ex)
$ python3 condprob.py logs/origin/ 0.05 0.7 > cond_origin_0.05_0.7.csv

plot.py
Generate (low conf, big conf) pairs
$ python3 plot.py [log dir]
Ex)
$ python3 plot.py logs/origin/ > plot_origin.csv

blanalyze.py
Calculate accuracy of bigLITTLE due to thresholds
$ python3 blanalyze.py [log dir]
Ex)
$ python3 blanalyze.py logs/origin/ > bl_origin.csv
