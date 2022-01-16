#!/bin/bash

stress-ng --metrics --cpu 2 -t 60 &
python3 monalyza.py stress-ng

stress-ng --metrics --cpu 2 -t 60
