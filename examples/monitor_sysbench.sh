#!/bin/bash

OUTPUT_DIR="./output/sysbench"
mkdir -p $OUTPUT_DIR
sysbench --test=cpu --time=60 run >> $OUTPUT_DIR/output.txt &
python3 monalyza/main.py sysbench
