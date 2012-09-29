#!/bin/bash

check(){
    if [[ "$?" -ne "0" ]]
    then
        echo "$0 FAILED"
        exit 1
    fi
}

virtualenv python_env
. python_env/bin/activate

pip install argparse==1.2.1
check
pip install numpy==1.6.2
check
pip install scipy==0.10.1
check
pip install matplotlib==1.1.1
check
pip install wsgiref==0.1.2
check
pip install logilab-astng==0.24.0
check
pip install logilab-common==0.58.1
check
pip install pylint==0.25.2
check

echo "################################################################################"
echo "#"
echo "# The Python virtual environment is ready to use. To start it,"
echo "#"
echo "# $ . python_env/bin/activate"
echo "#"
echo "################################################################################"
