#!/bin/bash


# Getting package installed if it is not already
function getpkg() {
  thepackage=$1
  if [ `apt -qq list "$thepackage" 2>/dev/null | grep installed | wc -l` -eq "0" ]; then
    echo "$thepackage was not found. Installing..."
    apt-get install "$thepackage" || { echo "Package $thepackage could not be installed!"; exit 10; }
  fi
}

# Apt-install of needed packages
getpkg build-essential
getpkg libssl-dev
getpkg libffi-dev
getpkg python3
#getpkg python3-dev
getpkg python3-pip
getpkg virtualenv
getpkg python3-virtualenv

# Check if python has really been installed
python=`which python3`
if [[ "$?" -ne 0 ]];
then
  echo "Please, install Python 3 on your system and then try again"
  exit 1
fi


# Check the version of python
python_version=`python3 --version`
required_version="Python 3.6.6"
if [[ "$python_version" != "$required_version" ]];
then
  echo "Please, install $required_version on your system and then try again"
  exit 1
fi

# Create a venv with the right python
virtualenv -p "$python" venv
if [[ "$?" -ne 0 ]];
then
  echo "Failed to create virtual environment for python"
  exit 2
fi

. activate.sh
pip3 install -r requirements.txt
if [[ "$?" -ne 0 ]];
then
  echo "Failed to install python requirements"
  exit 3
fi
