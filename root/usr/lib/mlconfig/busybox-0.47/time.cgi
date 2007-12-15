#!/bin/sh

. $MLCONFIG/mlconfig.sh

month() {
        if [ "$1" = "$2" ] ; then
                echo "<option value=$1 selected>$3</option>"
        else
                echo "<option value=$1>$3</option>"
        fi
}

case "$AUTHORIZATION" in
root|readonly) 
                html_ok
                html_title "Set Time and Date"
                if [ "$S_BUTTON" = "Save" ] ; then
                        echo "<center><p align=center>Setting date: <b>"
                        date "$S_YEAR.$S_MONTH.$S_DAY-$S_HOUR:$S_MINUTE:00" 2>&1
                        if [ -x /usr/sbin/hwclock ] ; then
                                hwclock --systohc --utc
                        fi
                        echo "</b></p></center>"
                fi

                echo "<form action=$SCRIPT_NAME><table align=center border=0>"
                echo "<tr><td align=right>Date:</td><td>"

                echo "<select name=DAY>"
                m=`date +%d`
                for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31
                do
                        if [ "$i" = "$m" ] ; then
                                echo "<option value=$i selected>$i</option>"
                        else
                                echo "<option value=$i>$i</option>"
                        fi
                done
                echo "</select>"

                echo "<select name=MONTH>"
                m=`date +%m`
                month 01 $m January
                month 02 $m February
                month 03 $m March
                month 04 $m April
                month 05 $m May
                month 06 $m June
                month 07 $m July
                month 08 $m August
                month 09 $m September
                month 10 $m October
                month 11 $m November
                month 12 $m December
                echo "</select>."

                echo "<input type=text name=YEAR size=4 maxsize=4 value=`date +%Y`>."
                echo "</td></tr>"
                
                echo "<tr><td align=right>Time:</td><td>"
                echo "<select name=HOUR>"
                m=`date +%H`
                for i in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23
                do
                        if [ "$i" = "$m" ] ; then
                                echo "<option value=$i selected>$i</option>"
                        else
                                echo "<option value=$i>$i</option>"
                        fi
                done
                echo "</select>:"
                echo "<select name=MINUTE>"
                m=`date +%M`
                for i in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 \
                         30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 
                do
                        if [ "$i" = "$m" ] ; then
                                echo "<option value=$i selected>$i</option>"
                        else
                                echo "<option value=$i>$i</option>"
                        fi
                done
                echo "</select>"
                echo "</td></tr><tr><td>&nbsp;</td><td><small><i>Note: if your system has been configured<br>to use a timeserver the time will be reset<br>whenever you connect to the network.</i></small></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=submit name=BUTTON value=\"Save\"></td></tr></table></form>"
                ;;

*)              html_authorization_required
                ;;
esac

