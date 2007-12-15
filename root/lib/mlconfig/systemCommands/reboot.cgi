#!/bin/sh

. $MLCONFIG/mlconfig.sh

case "$AUTHORIZATION" in
root|readonly) 
                if html_form_confirm "Reboot Midori" "Reboot NOW"
                then
                        reboot
                fi
                ;;

*)              html_authorization_required
                ;;
esac

