#!/bin/bash

# Move to the directory where your Python script is located
cd /Users/Maryna/Documents/RickMorty/

# Activate virtual environment if necessary
# source /path/to/your/venv/bin/activate

# Run the Python script with the full path and redirect output to a log file
/usr/bin/python3 main.py > /Users/Maryna/Documents/RickMorty/cron_log.txt 2>&1
