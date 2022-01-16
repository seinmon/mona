#!/bin/bash

OUTPUT_DIR="./output/stress-ng"
mkdir -p $OUTPUT_DIR
stress-ng --metrics --cpu 2 -t 60 >> $OUTPUT_DIR/output.txt &
python3 monalyza.py stress-ng
