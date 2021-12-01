#!/bin/bash

mkdir -p ~/Monalyza/output/
stress-ng --cpu 2 -t 60 >> ~/Monalyza/sysbench_output.txt &
python3 monalyza/main.py stress-ng
