SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
IPADDRESS=$SCRIPT_DIR/network_deploy/all_ip

: > $SCRIPT_DIR/network_deploy/ssh_known_hosts

ssh-keyscan -f $IPADDRESS -T 30 >> $SCRIPT_DIR/network_deploy/ssh_known_hosts
