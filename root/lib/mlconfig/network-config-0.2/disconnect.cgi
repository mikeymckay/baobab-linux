#!/bin/sh

. $MLCONFIG/mlconfig.sh

case "$AUTHORIZATION" in
root|readonly) 
                if html_form_confirm "Disconnect from Network" "Disconnect"
                then
                        html_ok
                        html_title "Disconnecting...."
                        cd /
                        /sbin/network stop > /dev/tty4 2>&1
                        echo "<big>The network has been disconnected</big>"
                        html_footer
                fi
                ;;

*)              html_authorization_required
                ;;
esac

