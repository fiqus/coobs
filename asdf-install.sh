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

# Install python requirements
make install-requirements

# Install node dependencies
make install-frontend

# Copy the settings template
cp coobs/settings/dev.template.py coobs/settings/dev.py

# Generate secret key for django and update it at coobs/settings.py
sed -i "s!SECRET_KEY = .*!SECRET_KEY = '$(openssl rand -base64 32)'!g" coobs/settings/dev.py

# Start postgres and create the database's user
pg_ctl start
sudo -iu postgres bash -c "psql -c \"CREATE USER coobs WITH PASSWORD 'coobspass';\""
sudo -iu postgres bash -c "psql -c \"ALTER ROLE coobs SET client_encoding TO 'utf8';\""
sudo -iu postgres bash -c "psql -c \"ALTER ROLE coobs SET default_transaction_isolation TO 'read committed';\""
sudo -iu postgres bash -c "psql -c \"ALTER ROLE coobs SET timezone TO 'UTC';\""
sudo -iu postgres bash -c "psql -c \"ALTER USER coobs CREATEDB;\""

# @TODO Configure db parameters at coobs/settings/dev.py

# Create the DB, run migrations and create django superuser
make reset-db

# Done!
echo "Installation done!"
echo "Run server:   make server"
echo "Run frontend: make frontend"
