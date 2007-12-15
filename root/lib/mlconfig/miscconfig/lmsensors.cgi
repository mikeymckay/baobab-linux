#!/bin/sh

. $MLCONFIG/mlconfig.sh

html_ok
html_title "Hardware Monitor"
echo "<h1>Current system status:</h1>"
/bin/date
echo "<p><pre>"
/usr/bin/sensors
echo "</pre></p>"
echo "<p>You can also get this info from the command line with 'sensors'</p>"
html_footer
