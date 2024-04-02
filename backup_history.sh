#!/bin/sh

# Directory to store backups
backup_dir="$HOME/.filtered-graphs"

# Create directory if it doesn't exist
mkdir -p "$backup_dir"

# Get current date and time for unique naming
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

# Backup filename
backup_file="$backup_dir/history_backup_$timestamp.txt"

echo "Backing up history to $backup_file..."

# Copy history file to backup file
cp $(dirname "$0")/history.txt $backup_file