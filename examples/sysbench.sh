#!/bin/bash

sysbench --test=cpu --time=60 run &
python3 monalyza.py sysbench

sysbench --test=cpu --time=60 run
