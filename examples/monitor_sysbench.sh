#!/bin/bash

mkdir -p ~/Monalyza/output/
sysbench --test=cpu --time=180 run >> ~/Monalyza/sysbench_output.txt &
python3 monalyza/main.py sysbench
