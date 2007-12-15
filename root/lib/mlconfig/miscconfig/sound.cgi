#!/bin/sh

. $MLCONFIG/mlconfig.sh

print_field() {
        echo "<tr><td align=right>$1:</td><td>"
        echo "<b>$2</b></td></tr>"
}

edit_field() {
        echo "<tr><td align=right>$1:</td><td>"
        echo "<input type=text name=$1 value=\"$2\"></td></tr>"
}

main_form() {
        . $CONFIG_WRITE/sound

        echo "<form action=$SCRIPT_NAME>"
        echo "<table align=center border=0>"
        echo "<tr><td colspan=2><h3>Sound Setup</h3></td></tr>"
        edit_field VOLUME "$VOLUME"
        edit_field PCM "$PCM"
        edit_field TREBLE "$TREBLE"
        edit_field BASS "$BASS"
        echo "<tr><td>&nbsp;</td><td><input type=submit value=Save name=BUTTON><input type=reset value=Reset></td></tr>"
        echo "</table>"
}

case "$AUTHORIZATION" in
root)
                html_ok
                html_title "Sound Configuration"
                cd $CONFIG_WRITE
		
		case "$S_BUTTON" in

                Save)
                        echo "VOLUME=\"$S_VOLUME\"" > sound
                        echo "PCM=\"$S_PCM\"" >> sound
                        echo "BASS=\"$S_BASS\"" >> sound
                        echo "TREBLE=\"$S_TREBLE\"" >> sound
                        $CONFIG_SAVE 2> /dev/null > /dev/null
			/usr/sbin/soundconfig
                        main_form
                        ;;
                *)
                        main_form
                        ;;
                esac
                html_footer

                ;;
readonly)
                html_ok
                html_title "Sound Configuration"
                . $CONFIG_WRITE/sound
                echo "<table align=center border=0>"
                echo "<tr><td colspan=2><h3>General Network Parameters</h3></td></tr>"
                print_field VOLUME "$VOLUME"
                print_field PCM "$PCM"
                print_field TREBLE "$TREBLE"
                print_field BASS "$BASS"
                echo "</table>"
                html_footer
                ;;

*)              html_authorization_required
                ;;
esac

