SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"

sudo bash -c "> $SCRIPT_DIR/keys/authorized_keys"
cd /home

for d in */; do
	user=$(echo -n $d | head -c -1)
	echo $user
	sudo mkdir /home/$user/.ssh
	sudo chmod 700 /home/$user/.ssh
	sudo chown $user:users /home/$user/.ssh
	sudo rm /home/$user/.ssh/id_rsa.pub
	sudo rm /home/$user/.ssh/id_rsa
	sudo ssh-keygen -f /home/$user/.ssh/id_rsa -t rsa -N '' -C $user 
	sudo chown $user:users /home/$user/.ssh/id_rsa
	sudo chown $user:users /home/$user/.ssh/id_rsa.pub
	sudo chmod 600 /home/$user/.ssh/id_rsa
	sudo chmod 700 /home/$user/.ssh/id_rsa.pub
	sudo rm /home/$user/.ssh/authorized_keys
	sudo cat /home/$user/.ssh/id_rsa.pub >> /home/$user/.ssh/authorized_keys
	sudo chown "$user":users /home/$user/.ssh/authorized_keys
	sudo chmod 600 /home/$user/.ssh/authorized_keys
done
