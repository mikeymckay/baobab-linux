#!/bin/sh

. $MLCONFIG/mlconfig.sh

# Get current version info
[ -f /etc/m4i.version ] && . /etc/m4i.version

CPU=`cat /proc/cpuinfo | sed -ne 's/cpu MHz.*: //p'`
CPU="$CPU MHz  `cat /proc/cpuinfo | sed -ne 's/model name.*: //p'`"
CPU="$CPU (`cat /proc/cpuinfo | sed -ne 's/cache size.*: //p'` cache)"

case "$AUTHORIZATION" in
root) 
                if [ "$S_HOSTPORT" = "" ] ; then
                        S_HOSTPORT=`cat /tmp/config/upgrade_host`
                fi
                if [ "$S_HOSTPORT" != "`cat /tmp/config/upgrade_host`" ] ; then
                        echo "$S_HOSTPORT" > /tmp/config/upgrade_host
                        freeze > /dev/null 2> /dev/null
                fi

                html_ok
                html_title "Upgrading"
		echo "<p>Your current configuration (as best as I can tell):"
		echo "<ul><li>CPU: <strong>$CPU</strong></li>"
		echo "<li>Current M4I version: <strong>$M4I_VERSION</strong></li>"
		echo "<li>Current M4I kernel: <strong>$M4I_KERNEL_CPU</strong></li>"
		echo "<li>Current M4I build date: <strong>$M4I_BUILD_DATE</strong></li></ul>"

		echo "<p><strong>WARNING!</strong> This upgrade will attempt to overwrite your flash disk with a new disk image. "
		echo "If you select an inappropriate image, or something goes wrong during the disk write, you could be left with a non-functional unit."
		echo "This code does not verify that the image you select is appropriate for your hardware.</p>"
		echo "Also, this upgrade will obliterate your current configuration."
		echo "If you have anything important in /config (eg. bookmarks), save it to another computer and copy it back after the upgrade.</p>"
		echo "<p><strong>YOU HAVE BEEN WARNED- PROCEED AT YOUR OWN RISK!</strong></p>"
			
                case "$S_BUTTON" in
                Upgrade)
                        echo "<b>X will be killed momentarily"
                        chvt 1
                        echo "[H[J" > /dev/tty1
                        x=$S_HOSTPORT
                        S_BUTTON= 
                        S_HOSTPORT=
                        export S_BUTTON S_HOSTPORT
                        /sbin/upgrade -h "$x" "$S_UPGRADE" > /dev/tty1 2> /dev/tty1
			sleep 3
			echo "Reboot now."
			exit 0
                        ;;

                Show\ Options)
                        echo "<p><center><form action=$SCRIPT_NAME><input type=hidden name=HOSTPORT value=\"$S_HOSTPORT\">"
                        echo "<select name=UPGRADE>"
                        for i in `/sbin/upgrade -h "$S_HOSTPORT"`
                        do
                        	echo "<option value=$i>$i</option>"
                        done
			echo "</select></center></p>"
			echo "<p><center><strong>THIS WILL OVERWRITE YOUR FLASH DISK!</strong></center></p>"
			echo "<p><center><input type=submit name=BUTTON value=\"Upgrade\"></center></form>"

                        ;;

                *) 
                        echo "<center><p align=center><form action=$SCRIPT_NAME>Host: <input type=text name=HOSTPORT value=\"$S_HOSTPORT\"><br>"
                        echo "<input type=submit name=BUTTON value=\"Show Options\"> <input type=reset value=\"Reset\"></form>"
                        ;;
                esac
                html_footer
                ;;

*)              html_authorization_required
                ;;
esac

