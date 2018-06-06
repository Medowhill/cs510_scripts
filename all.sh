for d in $(find $1 -maxdepth 1 -type d ! -path $1)
do
    echo python3 blanalyze.py $d
    python3 blanalyze.py $d
done
