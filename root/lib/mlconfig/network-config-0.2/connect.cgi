#!/bin/sh

. $MLCONFIG/mlconfig.sh

case "$AUTHORIZATION" in
root|readonly) 
                if html_form_confirm "Connect Network" "Connect Network"
                then
                        html_ok
                        html_title "Reconnecting...."
                        cd /
                        /sbin/network stop > /dev/tty4 2>&1
                        sleep 1
                        /sbin/network start > /dev/tty4 2>&1
                        echo "<big>You should now be reconnected to the network</big>"
                        html_footer
                fi
                ;;

*)              html_authorization_required
                ;;
esac
