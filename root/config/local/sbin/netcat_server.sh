#!/bin/sh
while true 
  do
    netcat -l -p4242 > /dev/lp0
done
