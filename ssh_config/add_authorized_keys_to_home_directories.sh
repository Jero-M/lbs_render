KNOWN_HOSTS="/home/jmaggi/.ssh/known_hosts"

cd /home

for d in */; do
	echo "$d"
	sudo mkdir /home/$d/.ssh
	sudo cp -f /home/jmaggi/.ssh/known_hosts /home/$d/.ssh
done
