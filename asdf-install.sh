#!/bin/bash

##
## Development environment installation using asdf
## https://github.com/asdf-vm/asdf
##

# Install required packages
sudo apt update -y
sudo DEBIAN_FRONTEND=noninteractive apt install -y sqlite3 sqlitebrowser \
  linux-headers-$(uname -r) build-essential software-properties-common automake autoconf make cmake \
  gpg bc m4 bzip2 dirmngr curl locate zlib1g-dev libssh-dev libssl-dev libncurses5-dev libsqlite3-dev libbz2-dev

# Add plugins and install following .tool-versions
asdf plugin-add python
asdf plugin-add postgres
asdf plugin-add nodejs
bash ~/.asdf/plugins/nodejs/bin/import-release-team-keyring
asdf install
asdf reshim

# Install pip tools
pip install --upgrade pip
pip install virtualenvwrapper

# Create virtualenv
mkvirtualenv coobs

# Setup python ENV vars at ~/.bash_aliases
VENVWRAPPER=$(locate virtualenvwrapper.sh)
tee -a $HOME/.bash_aliases <<TXT
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/projects
source $(echo $VENVWRAPPER)
TXT
source $HOME/.bash_aliases

# Install the requirements
pip install -r requirements.txt

# Copy the settings template
cp coobs/settings.template.py coobs/settings.py

# Generate secret key for django and update it at coobs/settings.py
SECRET_KEY=$(python manage.py generate_secret_key)
sed -i "s/SECRET_KEY = .*/SECRET_KEY = '${SECRET_KEY}'/g" coobs/settings.py

# Start postgres and create the DB
pg_ctl start
sudo su - postgres
psql -c "CREATE DATABASE coobs;"
psql -c "CREATE USER coobs WITH PASSWORD 'coobspass';"
psql -c "ALTER ROLE coobs SET client_encoding TO 'utf8';"
psql -c "ALTER ROLE coobs SET default_transaction_isolation TO 'read committed';"
psql -c "ALTER ROLE coobs SET timezone TO 'UTC';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE coobs TO coobs;"
exit

# @TODO Configure db parameters at coobs/settings.py


# Run database migrations
make migration

# Create a superuser
python manage.py createsuperuser

# Install node dependencies:
make frontend-install

# Done!
echo "Installation done!"
echo "Run server:   make server"
echo "Run frontend: make frontend"
