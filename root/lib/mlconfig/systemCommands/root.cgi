#!/bin/sh

. $MLCONFIG/mlconfig.sh

case "$AUTHORIZATION" in
root) 
                case "$S_CONSOLE" in
                3|4|5|6|7|8)
                        html_ok
                        html_title "Console is open"
                        echo "<pre>"
                        set -x
                        spawn /dev/tty"$S_CONSOLE" 0 0 /bin/sh -i &
                        sleep 1
                        chvt "$S_CONSOLE"
                        set +x
                        echo "</pre>"
                        html_footer
                        ;;
                *)
                        html_ok
                        html_title "Open Root Console" "Select Virtual Screen for Console:"
                        echo "<center><p align=center><form action=$SCRIPT_NAME><select name=CONSOLE>"
                        for i in 3 4 5 6 7 8
                        do
                                echo "<option value=$i>$i</option>"
                        done
                        echo "</select><input type=submit value=\"Open Console\" name=OK></form></p></center>"
                        echo "<pre>"
                        env
                        echo "</pre>"

                esac
                html_footer
                ;;

readonly)	html_forbidden
		;;

*)              html_authorization_required
                ;;
esac

