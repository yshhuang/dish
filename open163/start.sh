#!/bin/bash
source /etc/profile
cd /Volumes/develop/code-repository/python/dish/open163
echo "【`date +%Y-%m-%d_%H:%M:%S`】start open163 crawler"
python3 crawler_latest.py
echo "【`date +%Y-%m-%d_%H:%M:%S`】completed."
