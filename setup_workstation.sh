#!/bin/bash

if [[ "$UID" -ne "0" ]]
then
    echo "Certain commands in this script require root privileges."
    echo "Run as root or using sudo:"
    echo
    echo " $ sudo ./setup_workstation.sh"
    echo
    exit 1
fi

apt-get install python-pip
pip install virtualenv
apt-get build-dep python-scipy python-numpy
