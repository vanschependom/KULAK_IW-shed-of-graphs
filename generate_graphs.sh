
tic=`date +%s`

order=$1
filter_file=$2

# default value for number of threads
nb_of_threads=1

# check if third argument is not empty
# if it isn't we should check if the amount of threads is legal
if [ -n "$3" ];
    then
        nb_of_threads=$3
        # Check if the given argument is a positive integer between 1 and the number of cores
        if ! [[ $nb_of_threads =~ ^[0-9]+$ ]] || [ $nb_of_threads -le 0 ];
            then
                echo "Number of threads is not a positive integer. Please enter a positive integer."
                exit 1
            else
                if [ $nb_of_threads -eq 1 ];
                    then
                        echo "Generating graphs with $nb_of_threads thread."
                    else
                        echo "Generating graphs with $nb_of_threads threads."
                fi
        fi
fi

processes=()

# make a date string in the format of YYYY-MM-DD-HH-MM-SS
date=$(date +'%Y-%m-%d-%H-%M-%S')

# run the plantri command for each thread
for ((i=0; i<nb_of_threads; i++)); do
    ./plantri -p -g $order $i/$nb_of_threads 2>/dev/null | python3 filter_graphs.py $filter_file $date $i &
    # run the command in the background and save the process id
    processes+=($!)
done

# wait for all tasks to finish
for process in "${processes[@]}"; do
    wait $process
done

# run write_history.py
python3 write_history.py $date $filter_file $nb_of_threads

toc=$(date +%s)

echo "Generated all graphs."

times