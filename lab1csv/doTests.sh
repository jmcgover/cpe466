#! /bin/bash

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

CSV_FOLD="./csv-files/"
TXT_FOLD="./txt-files/"

echo "CSV FILES"
for file in $(ls ${CSV_FOLD}); do
        echo "~~~~~~~~~~~~"
        echo ${file}
        ./run.py --file ${CSV_FOLD}${file} --top 5 --length 0 --dot 0 1 --euclidean 0 1 --manhattan 0 1 --pearson 0 0 --max-row 0 --min-row 0 --median-row 0 --mean-row 0 --max-col 1 --min-col 1 --median-col 1 --mean-col 1 --quiet
done

echo "TEXT FILES"
for file in $(ls ${TXT_FOLD}); do
        echo "~~~~~~~~~~~~"
        echo ${file}
        ./run.py --file ${TXT_FOLD}${file} --top 5 --most-frequent --is-in grass --above 300 -w The,banana,pancakes,are,delicious --stats
done
exit


