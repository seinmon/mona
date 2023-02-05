#!/bin/bash

stress-ng --metrics --cpu 2 -t 60 &
mona stress-ng
