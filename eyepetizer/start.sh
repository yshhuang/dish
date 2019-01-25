#!/bin/bash
source /etc/profile
cd /Volumes/develop/code-repository/python/dish/eyepetizer
echo "【`date +%Y-%m-%d_%H:%M:%S`】start eyepetizer crawler"
python3 video.py
echo "【`date +%Y-%m-%d_%H:%M:%S`】eyepetizer completed."
