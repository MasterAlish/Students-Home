echo "Starting server at:"
ifconfig | grep  "inet "
echo "PORT: 8099"
echo
echo "Press CTRL+C to exit"

uwsgi --ini uwsgi.ini &>/dev/null
