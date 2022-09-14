#!/bin/bash

template="templates/ardine_protocol.md"
users="/tmp/users.json"
stats_folder="res/stats"

log_day=$(date --date="now" +"%Y-%m-%d")
log_timestamp=$(date --date="now" +"%H_%M_%S")
log_folder="res/logs/$log_day"
log="$log_folder/$log_timestamp.txt"

if [ ! -d "$log_folder" ];
then
  mkdir $log_folder
fi

# python scripts/mass_message_users.py --template $template --users $users --stats-folder $stats_folder 2>&1 >$log
python scripts/mass_message_users.py --template $template --users $users --stats-folder $stats_folder
