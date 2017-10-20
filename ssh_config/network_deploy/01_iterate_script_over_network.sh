SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
IPADDRESS=`cat $SCRIPT_DIR/all_ip`
RUNSCRIPT=$SCRIPT_DIR/restart_ssh_service.sh

stty -echo
read -p 'Enter the Lost Boys Staff Password:' PASSW
stty echo

for address in $IPADDRESS
do
  echo "\nWill run script on $address ...\n"
  gnome-terminal -x $SCRIPT_DIR/02_ssh_and_execute_script $PASSW $address $RUNSCRIPT
done
