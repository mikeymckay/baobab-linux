#!/bin/sh

. $MLCONFIG/mlconfig.sh

print_name() {
        echo "<tr><td align=right>$1:</td><td>"
}

print_field() {
        print_name "$1"
        echo "<b>$2</b></td></tr>"
}

edit_field() {
        print_name "$1"
        echo "<input type=text name=$1 value=\"$2\"></td></tr>"
}

edit_device_field() {
        print_name "$1"
        echo "&nbsp;</td><td><input type=text name=$1 value=\"$2\"></td></tr>"
}

main_form() {
        . $CONFIG_WRITE/network
        cd  $CONFIG_WRITE/net

        echo "<form action=$SCRIPT_NAME>"
        echo "<table align=center border=0>"
        echo "<tr><td colspan=2><h3>General Network Parameters</h3></td></tr>"
        edit_field HOSTNAME "$HOSTNAME"
        edit_field DOMAIN "$DOMAIN"
        print_name FORWARD_IPV4
        echo "<select name=FORWARD_IPV4>"
        if [ "$FORWARD_IPV4" = true ] ; then
                echo "<option value=true selected>true</option>"
                echo "<option value=false>false</option>"
        else
                echo "<option value=true>true</option>"
                echo "<option value=false selected>false</option>"
        fi
        echo "</select></td></tr>"
        print_name GATEWAYDEV
        echo "<select name=GATEWAYDEV>"
        for i in * 
        do
                if [ "$GATEWAYDEV" = "$i" ] ; then
                        echo "<option value=\"$i\" selected>$i</option>"
                else
                        echo "<option value=\"$i\">$i</option>"
                fi
        done
        echo "</select>"
        edit_field TIMESERVER "$TIMESERVER"
        if [ ! -x /bin/rdate -a ! -x /usr/bin/rdate ] ; then
                echo "<tr><td colspan=2><small>Please note that the timeserver is ignored unless the program <tt>rdate</tt> is installed. Currently that program cannot be found on this system</td></tr>"
        fi
        echo "<tr><td>&nbsp;</td><td><input type=submit value=Save name=BUTTON><input type=reset value=Reset></td></tr>"
        echo "<tr><td colspan=2><h3>Devices</h3></td></tr>"
        print_name "Installed Devices"
        echo "<select name=DEVICE>"
        for i in * 
        do
                echo "<option value=\"$i\">$i</option>"
        done
        echo "</select><input type=submit name=BUTTON value=\"Edit Device\">"
        echo "<input type=submit name=BUTTON value=\"Delete Device\">"
        echo "</td></tr>"
        print_name "New Device"
        echo "<input type=text name=NEW><input type=submit name=BUTTON value=\"Create\"></td></tr>"
        echo "</table>"
}

edit_device() {
        cd $CONFIG_WRITE/net
        DEVICE=
        TYPE=
        ENABLED=
	DRIVER=
        IPADDR=
        DOMAIN=
        GATEWAY=
        NETWORK=
        NETMASK=
        BROADCAST=
        DNS=
	WLAN=
        WLAN_USER_MIBS=
        WLAN_SSID=
        WLAN_AUTHTYPE=
	WLAN_MODE=
	WLAN_WEP=
        WLAN_WEP_KEY_PHRASE=

        if [ -f "$1" ] ; then
                . "./$1"
        fi
	echo "<p><center><i><a href="$SCRIPT_NAME">back to network config page</a></i></center></p>"
        echo "<form action=$SCRIPT_NAME><input type=hidden name=DEVICE value=\"$DEVICE\">"
        echo "<table align=center border=0>"
        echo "<tr><td colspan=3><h3>Device $1</h3></td></tr>"
        
        print_name "ENABLED"
        if [ "$ENABLED" = "y" ] ; then
                echo "<input type=radio name=ENABLED value=y checked></td><td><b>yes</b></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=radio name=ENABLED value=n></td><td><b>no</b></td></tr>"
        else
                echo "<input type=radio name=ENABLED value=y></td><td><b>yes</b></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=radio name=ENABLED value=n checked></td><td><b>no</b></td></tr>"
        fi
        edit_device_field DRIVER "$DRIVER"
        print_name "TYPE"
        if [ "$TYPE" = static ] ; then
                echo "<input type=radio name=TYPE value=dhcp></td><td><b>dhcp</b></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=radio name=TYPE value=static checked></td><td><b>static</b></td></tr>"
        else
                echo "<input type=radio name=TYPE value=dhcp checked></td><td><b>dhcp</b></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=radio name=TYPE value=static></td><td><b>static</b></td></tr>"
        fi
        edit_device_field IPADDR "$IPADDR"
        edit_device_field DOMAIN "$DOMAIN"
        edit_device_field GATEWAY "$GATEWAY"
        edit_device_field NETWORK "$NETWORK"
        edit_device_field NETMASK "$NETMASK"
        edit_device_field BROADCAST "$BROADCAST"
        edit_device_field DNS "$DNS"
        print_name "WLAN"
        if [ "$WLAN" = "y" ] ; then
                echo "<input type=radio name=WLAN value=y checked></td><td><b>yes</b></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=radio name=WLAN value=n></td><td><b>no</b></td></tr>"
        else
                echo "<input type=radio name=WLAN value=y></td><td><b>yes</b></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=radio name=WLAN value=n checked></td><td><b>no</b></td></tr>"
        fi
        edit_device_field WLAN_USER_MIBS "$WLAN_USER_MIBS"
        edit_device_field WLAN_SSID "$WLAN_SSID"
        edit_device_field WLAN_AUTHTYPE "$WLAN_AUTHTYPE"
	print_name "WLAN_MODE"
	if [ "$WLAN_MODE" = "adhoc" ] ; then
	    echo "<input type=radio name=WLAN_MODE value=infrastructure></td><td><b>infrastructure</b></td></tr>"
	    echo "<tr><td>&nbsp;</td><td><input type=radio name=WLAN_MODE value=adhoc checked></td><td><b>adhoc</b></td></tr>"
    	else
            echo "<input type=radio name=WLAN_MODE value=infrastructure checked></td><td><b>infrastructur
	    e</b></td></tr>"
	    echo "<tr><td>&nbsp;</td><td><input type=radio name=WLAN_MODE value=adhoc></td><td><b>adhoc</b></td></tr>"
    	fi
	print_name "WLAN_WEP"
	case "$WLAN_WEP" in
	64bit)
		echo "<input type=radio name=WLAN_WEP value=none></td><td><b>none</b></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=radio name=WLAN_WEP value=64bit checked></td><td><b>64bit (aka 40bit)</b></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=radio name=WLAN_WEP value=128bit></td><td><b>128bit (aka 104 bit)</b></td></tr>"
	;;
	128bit)
		echo "<input type=radio name=WLAN_WEP value=none></td><td><b>none</b></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=radio name=WLAN_WEP value=64bit></td><td><b>64bit (aka 40bit)</b></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=radio name=WLAN_WEP value=128bit checked></td><td><b>128bit (aka 104 bit)</b></td></tr>"
		;;
	*)
		echo "<input type=radio name=WLAN_WEP value=none checked></td><td><b>none</b></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=radio name=WLAN_WEP value=64bit></td><td><b>64bit (aka 40bit)</b></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=radio name=WLAN_WEP value=128bit></td><td><b>128bit (aka 104 bit)</b></td></tr>"
	;;
	esac
        edit_device_field WLAN_WEP_KEY_PHRASE "$WLAN_WEP_KEY_PHRASE"

        echo "<tr><td>&nbsp;</td><td colspan=2><input type=submit name=BUTTON value=\"Save Device\"><input type=reset value=Reset></td></tr></table>"
	echo "<p><center><i><a href="$SCRIPT_NAME">back to network config page</a></i><center></p>"
}

case "$AUTHORIZATION" in
root)
                html_ok
                html_title "Network Configuration"
                cd $CONFIG_WRITE

                case "$S_BUTTON" in
                Create)
                        cd $CONFIG_WRITE/net
                        echo "DEVICE=\"$S_NEW\"" > "$S_NEW"
                        echo "TYPE=\"dhcp\"" >> "$S_NEW"
                        if [ -f "$S_NEW" ] ; then
                                edit_device "$S_NEW"
                        else 
                                main_form
                        fi
                        
                        ;;
                Edit\ Device)
                        cd $CONFIG_WRITE/net
                        if [ -f "$S_DEVICE" ] ; then
                                edit_device "$S_DEVICE"
                        else 
                                main_form
                        fi
                        ;;
                Save\ Device)
                        cd $CONFIG_WRITE/net
                        if [ -f "$S_DEVICE" ] ; then
                                echo "DEVICE=\"$S_DEVICE\"" > $S_DEVICE
                                echo "TYPE=\"$S_TYPE\"" >> $S_DEVICE
                                echo "ENABLED=\"$S_ENABLED\"" >> $S_DEVICE
                                echo "DRIVER=\"$S_DRIVER\"" >> $S_DEVICE
                                echo "IPADDR=\"$S_IPADDR\"" >> $S_DEVICE
                                echo "DOMAIN=\"$S_DOMAIN\"" >> $S_DEVICE
                                echo "GATEWAY=\"$S_GATEWAY\"" >> $S_DEVICE
                                echo "NETWORK=\"$S_NETWORK\"" >> $S_DEVICE
                                echo "NETMASK=\"$S_NETMASK\"" >> $S_DEVICE
                                echo "BROADCAST=\"$S_BROADCAST\"" >> $S_DEVICE
                                echo "DNS=\"$S_DNS\"" >> $S_DEVICE
                                echo "WLAN=\"$S_WLAN\"" >> $S_DEVICE
                                echo "WLAN_USER_MIBS=\"$S_WLAN_USER_MIBS\"" >> $S_DEVICE
                                echo "WLAN_SSID=\"$S_WLAN_SSID\"" >> $S_DEVICE
                                echo "WLAN_AUTHTYPE=\"$S_WLAN_AUTHTYPE\"" >> $S_DEVICE
                                echo "WLAN_MODE=\"$S_WLAN_MODE\"" >> $S_DEVICE
				echo "WLAN_WEP=\"$S_WLAN_WEP\"" >> $S_DEVICE
                                echo "WLAN_WEP_KEY_PHRASE=\"$S_WLAN_WEP_KEY_PHRASE\"" >> $S_DEVICE
                                $CONFIG_SAVE 2> /dev/null > /dev/null
                                edit_device "$S_DEVICE"
                        else
                                main_form
                        fi
                        ;;

                Delete\ Device)
                        if [ -f "net/$S_DEVICE" ] ; then
                                rm "net/$S_DEVICE"
                        fi
                        main_form
                        ;;
                Save)
                        echo "HOSTNAME=\"$S_HOSTNAME\"" > network
                        echo "DOMAIN=\"$S_DOMAIN\"" >> network
                        echo "FORWARD_IPV4=\"$S_FORWARD_IPV4\"" >> network
                        echo "GATEWAYDEV=\"$S_GATEWAYDEV\"" >> network
                        echo "TIMESERVER=\"$S_TIMESERVER\"" >> network
                        $CONFIG_SAVE 2> /dev/null > /dev/null
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
                html_title "Network Configuration"
                . $CONFIG_WRITE/network
                echo "<table align=center border=0>"
                echo "<tr><td colspan=2><h3>General Network Parameters</h3></td></tr>"
                print_field HOSTNAME "$HOSTNAME"
                print_field DOMAIN "$DOMAIN"
                print_field FORWARD_IPV4 "$FORWARD_IPV4"
                print_field GATEWAYDEV "$GATEWAYDEV"
                set -x
                cd $CONFIG_WRITE/net
                for i in * 
                do
                        . ./$i
                        echo "<tr><td colspan=2><h3><br>Device <b>$DEVICE</b></h3></td></tr>"
                        if [ "$TYPE" = static ] ; then
                                print_field TYPE static
                                print_field IPADDR "$IPADDR"
                                print_field DOMAIN "$DOMAIN"
                                print_field GATEWAY "$GATEWAY"
                                print_field NETWORK "$NETWORK"
                                print_field NETMASK "$NETMASK"
                                print_field BROADCAST "$BROADCAST"
                                print_field DNS "$DNS"
                        else
                                print_field TYPE dhcp
                        fi
                done
                echo "</table>"
                html_footer
                ;;

*)              html_authorization_required
                ;;
esac

