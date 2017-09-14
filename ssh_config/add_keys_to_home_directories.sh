SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
PUB_KEY=$SCRIPT_DIR/keys/id_rsa.pub
PRIV_KEY=$SCRIPT_DIR/keys/id_rsa

cd /home

for d in */; do
	user=$(echo -n $d | head -c -1)
	echo $user
	sudo mkdir /home/$user/.ssh
	sudo cp -f $PUB_KEY /home/$user/.ssh/id_rsa.pub
	sudo cp -f $PRIV_KEY /home/$user/.ssh/id_rsa
	sudo chown $user:users /home/$user/.ssh/id_rsa
done
