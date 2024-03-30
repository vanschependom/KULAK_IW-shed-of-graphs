#!/bin/bash

# Directory where backups are stored
backup_dir="$HOME/.filtered-graphs"

# Get a list of history backup files
backup_files=("$backup_dir"/history_backup_*.txt)

# Check if there are any backup files
if [ ${#backup_files[@]} -eq 0 ]; then
    echo "No history backup files found in the backup directory."
    exit 1
fi

# Display available backups
echo "These are the timestamps of all available backups:"
for ((i=0; i < ${#backup_files[@]}; i++)); do
    echo -e "\t $((i+1)). $(basename "${backup_files[$i]}" | sed 's/history_backup_//' | sed 's/.txt//')"
done

# Ask user to select a backup
while true; do
    echo ""
    read -p "Enter the number of the backup to be restored: " backup_number

    # Validate user input
    if ! [[ "$backup_number" =~ ^[0-9]+$ ]]; then
        echo "Invalid input. Please enter a number."
        continue
    fi

    # Check if the selected backup number is within the range
    if ((backup_number < 1 || backup_number > ${#backup_files[@]})); then
        echo "Invalid backup number. Please select a number within the range."
        continue
    fi

    break
done

# Get the selected backup file path
selected_backup="${backup_files[$((backup_number-1))]}"

echo ""

# Print the selected backup file path
echo "Selected backup file: $selected_backup"
echo "Restoring history from the selected backup..."

cp "$selected_backup" history.txt