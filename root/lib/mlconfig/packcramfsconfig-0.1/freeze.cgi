#!/bin/sh

. $MLCONFIG/mlconfig.sh

case "$AUTHORIZATION" in
root|readonly) 
                if html_form_confirm "Permanently Store Configuration" "Store Configuration"
                then
                        html_ok
                        html_title "Freezing configuration"
                        echo "<pre>"
                        $CONFIG_SAVE
                        echo "</pre>"
                        html_footer
                fi
                ;;

*)              html_authorization_required
                ;;
esac

