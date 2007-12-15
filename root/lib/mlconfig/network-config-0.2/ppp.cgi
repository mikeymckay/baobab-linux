#!/bin/sh

# Cobbled 2002 Julio Iglacias... input and basic template mostly from time.cgi... 
# The 

. $MLCONFIG/mlconfig.sh

case "$AUTHORIZATION" in
root|readonly) 
                html_ok
                html_title "Modem Setup"
                if [ "$S_BUTTON" = "Save" ] ; then
                        echo "<center><p align=center><b>Saving Modem Settings</b>"
                        if [ -f /tmp/config/.eznet/eznet.conf ] ; then
                                eznet delete 0
                        fi
			eznet add service=ppp user=$S_NAME password=$S_PASS phone=$S_PHONE
             
	     #set up /etc/resolv.conf -- code pinched from /sbin/ifup
	    		if [ "$S_DNS" != "" ] ; then                                                                        
			    for i in $S_DNS                                                                             
			    do                                                                                        
			    	    echo nameserver $i                                                                
			    done >> /etc/ppp.resolv.conf
			fi                                              
	     # </pinch>        
			#dramatic display.. optional
	        	sleep 1
			echo "<BR>Saving Username ..&nbsp;$S_NAME&nbsp;<img src='../green.gif' border=0>"
			echo "<BR>Saving Password ..&nbsp;$S_PASS&nbsp;<img src='../green.gif' border=0>"
			echo "<BR>Saving Phone Number ..&nbsp;$S_PHONE&nbsp;<img src='../green.gif' border=0>"
			#would be possible to loop like above for more effect
			echo "<BR>Saving DNS Server(s)..&nbsp;$S_DNS&nbsp;<img src='../green.gif' border=0>" 
			sleep 2
			#end drama
			
			echo "<BR><b><FONT COLOR='#1db617'>Settings Saved</FONT></b></p></center>"
                fi
                echo "<form action=$SCRIPT_NAME><table align=center border=0>"
                echo "<tr><td align=right>Username:</td><td>"
                echo "<input type=text name=NAME size=32 maxsize=32>"
                echo "</td></tr>"
                echo "<tr><td align=right>Password:</td><td>"
                echo "<input type=text name=PASS size=32 maxsize=32>"
                echo "</td></tr>"
                echo "<tr><td align=right>Phone Number:</td><td>"
                echo "<input type=text name=PHONE size=32 maxsize=32>"
		echo "</td></tr>"
		echo "<tr><td align=right>DNS Server(s):</td><td>"                                              
		echo "<input type=text name=DNS size=32 maxsize=256>"
                echo "</td></tr>"
                echo "<tr><td>&nbsp;</td><td><small><i>Note: if your system was configured<br>to use PPP before, those settings will be<br>replaced when you press the save button.</i></small></td></tr>"
                echo "<tr><td>&nbsp;</td><td><input type=submit name=BUTTON value=\"Save\"></td></tr></table></form><br><br>"
		echo "<center>Use the Networking menu to connect/disconnect.</center>"
                ;;

*)              html_authorization_required
                ;;
esac

