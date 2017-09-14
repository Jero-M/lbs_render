SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
IPADDRESS=`cat $SCRIPT_DIR/network_deploy/all_ip`

for address in $IPADDRESS
do
  echo "Will run script on $address ..."
  sleep 1
  ssh-keyscan $address >> $SCRIPT_DIR/known_hosts
done
