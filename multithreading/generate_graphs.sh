# the first argument should be the order of the graphs to be generated
# the second argument is the filter file
# number of threads is the first argument
threads=$1

# Check if the given argument is a positive integer
if ! [[ "$threads" =~ "^[0-9]+$" ]]
    then
        echo "Number of threads is not a positive integer. Please enter a positive integer."
		exit 1
fi


# array to keep track of all processes
processes=()

for ((i=0; i<threads; i++)); do
	# the second argument should be the order of the graphs to be generated
	# the third argument is the filter file
	./plantri -p -g $2 $i/$threads 2>/dev/null | python3 multithreading/filter_graphs.py $3 $i &
	processes+=($!)
done

# wait for all tasks to finish
for process in "${processes[@]}"; do
	wait $process
done

echo "Generated all graphs."

# Merge the histories of all threads
python3 multithreading/merge_history.py $threads

echo "Merged all history files."
