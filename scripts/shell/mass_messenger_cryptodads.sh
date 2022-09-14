#!/bin/bash

template="templates/crypto_dads.md"
users="res/users-200k.json"
stats_folder="res/stats"
media="res/video.mp4"

log_day=$(date --date="now" +"%Y-%m-%d")
log_timestamp=$(date --date="now" +"%H_%M_%S")
log_folder="res/logs/$log_day"
log="$log_folder/$log_timestamp.txt"

if [ ! -d "$log_folder" ];
then
  mkdir $log_folder
fi

python scripts/mass_message_users.py --template $template --users $users --stats-folder $stats_folder --media $media 2>&1 >$log
