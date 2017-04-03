#!/usr/bin/env bash

# one example of run.sh script for implementing the features using python
# the contents of this script could be replaced with similar files from any major language

# I'll execute my programs, with the input directory log_input and output the files in the directory log_output
# echo "Feature 1"
# python ./src/process_log_hosts.py --input ./log_input/log.txt --output ./log_output/hosts.txt 
# echo "Feature 2"
# python ./src/process_log_hours.py --input ./log_input/log.txt --output ./log_output/hours.txt 
# echo "Feature 3"
# python ./src/process_log_resources.py --input ./log_input/log.txt --output ./log_output/resources.txt 
# echo "Feature 4"
# python ./src/process_log_blocked.py --input ./log_input/log.txt --output ./log_output/blocked.txt 
# echo "Feature 5"
# python ./src/process_log_congested.py --input ./log_input/log.txt --output ./log_output/congested.txt 
# echo "Feature 6"
python ./src/process_log_resources_hours.py --input ./log_input/log.txt --resources ./log_output/resources.txt --output ./log_output/resources_hours.txt 
