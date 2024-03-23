# the first argument should be the order of the graphs to be generated
# the second argument is the filter file
./plantri -p -g $1 2>/dev/null | python3 filter_graphs.py $2