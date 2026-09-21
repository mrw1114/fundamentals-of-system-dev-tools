#!/bin/bash
cnt=0
while ./42.sh >> stdout.log 2>> stderr.log
do
    cnt=$((cnt+1))
done

echo "Failed after $cnt runs."

