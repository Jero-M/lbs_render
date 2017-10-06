SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
KNOWN_HOSTS=$SCRIPT_DIR/network_deploy/ssh_known_hosts

cd /home

for d in */; do
	user=$(echo -n $d | head -c -1)
	echo $user
	sudo mkdir /home/$user/.ssh
	sudo chmod 700 /home/$user/.ssh
	sudo chown $user:users /home/$user/.ssh
	sudo cp -f $KNOWN_HOSTS /home/$user/.ssh/known_hosts
	sudo chown "$user":users /home/$user/.ssh/known_hosts
	sudo chmod 644 /home/$user/.ssh/known_hosts
done
