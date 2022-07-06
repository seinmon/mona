#!/bin/bash

stress-ng --metrics --cpu 2 -t 60 &
python3 mona.py stress-ng
