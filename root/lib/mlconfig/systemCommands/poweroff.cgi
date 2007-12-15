#!/bin/sh

. $MLCONFIG/mlconfig.sh

case "$AUTHORIZATION" in
root|readonly) 
                if html_form_confirm "Power Off Midori" "Power Off NOW"
                then
                        halt
                fi
                ;;

*)              html_authorization_required
                ;;
esac

