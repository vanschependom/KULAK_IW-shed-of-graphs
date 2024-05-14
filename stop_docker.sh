#!/bin/bash

# Docker container ID is the first argument
container_id=$1

{
    #try
    # Copy the history file to the working directory
    docker cp $container_id:app/history.txt . 2>/dev/null

    # Stop the container
    docker stop $container_id 1>/dev/null 2>/dev/null
} || {
    #except when we get errors above because the ID is not valid.
    echo "Container ID is not a valid container ID. Please provide a valid container ID." 
    exit 1
}

echo "Copied history file."
echo "Stopped docker container with ID:" $container_id
exit 0



