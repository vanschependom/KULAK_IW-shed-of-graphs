import os
import sys
from datetime import datetime

def merge_history(amount_of_threads):
    
    history = list()
    
    for i in range(amount_of_threads):
        file = open(f"multithreading/history_{i}.txt", "r")
        for j in file.read().split("\n"):
            history.append(j)
        file.close()
    
    try:
        # Make a new file with the name history.txt
        file = open(f"history.txt", "x+")
    except:
        # If the above code gives an error, (because the file already exists) append to the file
        file = open(f"history.txt", "a")
        
    for i in history:
        if i != "":
            file.write(i+"\n")
    file.close()

    
if __name__ == "__main__":
    amount_of_threads = int(sys.argv[1])
    merge_history(amount_of_threads)