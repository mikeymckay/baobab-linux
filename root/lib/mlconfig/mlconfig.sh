# list of useful functions for shell cgi scripts

BG_COLOR=ffffff

html_title() {
        t=$2
        [ "$2" != "" ] || t=$1
        echo "<html><head><title>$1</title></head>"
	echo "<body bgcolor=$BG_COLOR>"
	echo "<h1 align=center>$t</h1>"
}

html_header() {
        echo "HTTP/1.0 $1"
        echo "Connection: close"
        echo "Content-type: text/html"
        shift
        for i do
                echo "$i"
        done
        echo
}

html_footer() {
        echo "<center><p align=center><a href=/ target=_top><i>Main menu</i></p></center></body></html>"
}

html_authorization_required() {
        html_header "401 Authorization Required" "WWW-Authenticate: Basic realm=$BASIC_REALM"
        html_title "Authorization Required" "Authorization Required"
        html_footer
        exit 0
}

html_forbidden() {
        html_header "403 Forbidden"
        html_title "Forbidden" "You are not allowed to do this"
        html_footer
        exit 1
}

# returns 0 if command should be executed
# $1=page title
# $2=string on button
html_form_confirm() {
        if [ "$S_OK" = "" ] ; then
                html_ok
                html_title "$1" "$1?"
                echo "<center><p align=center><form action=$SCRIPT_NAME><input type=submit value=\"$2\" name=OK></form></p></center>"
                html_footer
                return 1
        fi
        return 0
}

html_ok() {
        html_header "200 OK"
}
