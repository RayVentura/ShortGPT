#!/bin/bash

log=$(date +%s)
rm *.log
python3 ultra.py >> $log.log &&
python3 final_upload.py >> $log.log &&

echo "run"
