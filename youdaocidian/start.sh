#!/bin/bash
source /etc/profile
cd /Volumes/develop/code-repository/python/dish/youdaocidian
echo "【`date +%Y-%m-%d_%H:%M:%S`】start youdao_dict crawler"
python3 save-to-mongodb.py
echo "【`date +%Y-%m-%d_%H:%M:%S`】completed."
