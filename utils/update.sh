#!/bin/sh
# Change INSTALLDIR to your needs. It currently points to your desktop
# the library's directory pyARTE should be placed at the same directory.
INSTALLDIR=~/Escritorio/pyARTE
#PIP=~/Applications/venv/bin/pip

while [ "$(hostname -I)" = "" ]; do
  echo -e "\e[1A\e[KNo network: $(date)"
  sleep 1
done

echo "I have network"
echo "Internet is reachable"

# none reachable
echo "Internet is up"
echo "Updating repos"

# update repos
cd $INSTALLDIR
git stash
git stash clear
git pull

# now install packages
#pip install -r requirements.txt


echo "Process ended correctly on
date
