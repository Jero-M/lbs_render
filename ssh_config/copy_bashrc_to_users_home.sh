SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
BASHRC_PATH=$SCRIPT_DIR/.bashrc

cd /home

for d in */; do
	user=$(echo -n $d | head -c -1)
	echo $user
	sudo cp -f $BASHRC_PATH /home/$user/.bashrc
	sudo chown "$user":users /home/$user/.bashrc
	sudo chmod 600 /home/$user/.bashrc
done
