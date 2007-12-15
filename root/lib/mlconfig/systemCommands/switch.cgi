#!/bin/sh

. $MLCONFIG/mlconfig.sh

case "$AUTHORIZATION" in
root|readonly) 
                case "$S_SWITCH" in
                1|2|3|4|5|6|7|8)
                        html_ok
                        html_title "Switch Done"
                        chvt "$S_SWITCH"
                        html_footer
                        ;;
                *)
                        html_ok
                        html_title "Switch Screen" "Select Screen To Switch To:"
                        echo "<center><p align=center><form action=$SCRIPT_NAME><select name=SWITCH>"
                        for i in 1 2 3 4 5 6 7 8
                        do
                                echo "<option value=$i>$i</option>"
                        done
                        echo "</select><input type=submit value=\"Switch\" name=OK></form></p></center>"
                esac
                html_footer
                ;;

*)              html_authorization_required
                ;;
esac

