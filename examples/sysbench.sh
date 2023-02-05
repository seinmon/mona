#!/bin/bash

sysbench --test=cpu --time=60 run &
mona sysbench
