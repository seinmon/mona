#!/bin/bash

sysbench --test=cpu --time=60 run &
python3 mona.py sysbench
