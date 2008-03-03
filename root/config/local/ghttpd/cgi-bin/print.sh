#!/bin/sh
printer_file="/tmp/print"
printer="/dev/lp0"

# First arg will be mode (start,continue or finish)
mode=`echo ${QUERY_STRING} | cut -d "&" -f 1 | cut -d "=" -f 2`
# Second arg will be print string
# Replace spaces, quotes and newlines
print_string=`echo ${QUERY_STRING} | cut -d "&" -f 2 | cut -d "=" -f 2 | sed "s/%20/ /g" | sed "s/%22/\"/g" | sed "s/%5C/\\\\\\/g" | sed "s/%0A/
/g"`

echo "Mode: $mode"
echo "Print string: $print_string"

if [ $mode = "start" ]; then
  echo -n "$print_string" > $printer_file
elif [ $mode = "continue" ]; then
  echo -n "$print_string" >> $printer_file
elif [ $mode = "finish" ]; then
  echo -n "$print_string" >> $printer_file
  #cat $printer_file > $printer
  cat $printer_file | netcat localhost 4242
else
  echo "No mode given"
fi
