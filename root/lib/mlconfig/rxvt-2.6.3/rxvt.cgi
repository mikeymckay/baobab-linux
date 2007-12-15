#!/bin/sh

. $MLCONFIG/mlconfig.sh

case "$AUTHORIZATION" in
root|readonly) 
                if html_form_confirm "Open RXVT Root Terminal" "Open RXVT"
                then
                        rxvt &
                        html_ok
                        html_title "RXVT Terminal has been opened" "RXVT Terminal has been opened"
                fi
                html_footer
                ;;

*)              html_authorization_required
                ;;
esac

