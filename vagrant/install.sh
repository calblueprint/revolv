#!/bin/bash

# Script to set up a Django project on Vagrant.
DATABASE_USERNAME="revolv"
DATABASE_PASSWORD="revolv"
DATABASE_NAME="revolv_db"

PGSQL_VERSION=9.3

# Need to fix locale so that Postgres creates databases in UTF-8
locale-gen en_GB.UTF-8
dpkg-reconfigure locales

export LANGUAGE=en_GB.UTF-8
export LANG=en_GB.UTF-8
export LC_ALL=en_GB.UTF-8

# Install essential packages from Apt
apt-get update -y
# Python dev packages
apt-get install -y build-essential python python-dev
# python-setuptools being installed manually
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python
# Dependencies for image processing with Pillow (drop-in replacement for PIL)
# supporting: jpeg, tiff, png, freetype, littlecms
# (pip install pillow to get pillow itself, it is not in requirements.txt)
apt-get install -y libjpeg-dev libtiff-dev zlib1g-dev libfreetype6-dev liblcms2-dev
# Git (we'd rather avoid people keeping credentials for git commits in the repo, but sometimes we need it for pip requirements that aren't in PyPI)
apt-get install -y git

# Postgresql
if ! command -v psql; then
    apt-get install -y postgresql-$PGSQL_VERSION libpq-dev
    cp /vagrant/vagrant/pg_hba.conf /etc/postgresql/$PGSQL_VERSION/main/
    /etc/init.d/postgresql reload
fi

# virtualenv global setup
if ! command -v pip; then
    easy_install -U pip
fi
if [[ ! -f /usr/local/bin/virtualenv ]]; then
    pip install virtualenv virtualenvwrapper stevedore virtualenv-clone
fi


# Node.js, CoffeeScript and LESS
if ! command -v npm; then
    sudo apt-get install -y node npm
fi

sudo apt-get install rubygems-integration
sudo gem install sass

sudo -u postgres psql -c "create database $DATABASE_NAME;"
sudo -u postgres psql -c "create user $DATABASE_USERNAME with password '$DATABASE_PASSWORD';"
sudo -u postgres psql -c "grant all privileges on database $DATABASE_NAME to $DATABASE_USERNAME;"
sudo -u postgres psql -c "alter user $DATABASE_USERNAME createdb;"

virtualenv venv
source venv/bin/activate
pip install -r /vagrant/requirements.txt
pre-commit install

sudo npm install -g grunt-cli
cd /vagrant && npm install

sudo npm install -g bower
cd /vagrant/revolv/static/ && bower install foundation
cd /vagrant && grunt sass
