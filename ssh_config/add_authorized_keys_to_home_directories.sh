SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
AUTH_KEYS=$SCRIPT_DIR/keys/authorized_keys

cd /home

for d in */; do
	user=$(echo -n $d | head -c -1)
	echo $user
	sudo mkdir /home/$user/.ssh
	sudo cp -f $AUTH_KEYS /home/$user/.ssh/authorized_keys
	sudo chown "$user":users /home/$user/.ssh/authorized_keys
done
