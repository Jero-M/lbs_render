SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
echo "Copying ssh_known_hosts to local /etc/ssh ... \n"

sudo cp -f $SCRIPT_DIR/ssh_known_hosts /etc/ssh/ssh_known_hosts

echo "ssh_known_hosts was successfully copied \n"

return

