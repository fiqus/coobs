# Cooperative social balance app 

## Running Backend

1. Create virtualenv using python3 (follow https://virtualenvwrapper.readthedocs.io/en/latest/install.html)

        mkvirtualenv coobs

2. Activate the virtualenv

        workon coobs

3. Install the requirements

        pip install -r requirements.txt

4. Copy the settings template

        cp coobs/settings.template.py coobs/settings.py

5. Generate new Django secret key and replace 'change-me' value for SECRET_KEY at coobs/settings.py

        python manage.py generate_secret_key

6. Create your postgres db

        sudo su postgres 
        psql
        CREATE DATABASE coobs;
        CREATE USER coobs WITH PASSWORD 'coobspass';
        ALTER ROLE coobs SET client_encoding TO 'utf8';
        ALTER ROLE coobs SET default_transaction_isolation TO 'read committed';
        ALTER ROLE coobs SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE coobs TO coobs;
        \q
        exit

7. Configure db parameters at coobs/settings.py

        DATABASES = {
                'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': 'coobs',
                        'USER': 'coobs',
                        'PASSWORD': 'coobspass',
                        'HOST': 'localhost',
                        'PORT': '5432'
                },
        }

8. Run database migrations

        python manage.py migrate

9. Create a superuser

        python manage.py createsuperuser

10. Run the server

        python manage.py runserver

11. API now should be accessible in:

        http://localhost:8000/api/

## Running Frontend

1. Install node dependencies:

        make frontend-install

2. Start the frontend app:
        
        make frontend

3. App core and landing page should be accesible on:

        http://localhost:8080/app
        http://localhost:8080/landing

## Frontend translations

### Adding new language

1. Go to `/coobs/frontend/locales` and add the new language in `langs.json` file

        key -> language short ISO code
        value -> language name

2. In the same folder add a new file with ISO code as name and `.json` extension

3. Add all existing translations for the new language.

### Adding new translation

1. Try to find if translation does not already exist.

2. Add new pair key/value in each translations file.

## Backend translations

### Adding new language

1. Add new locale file

        python manage.py makemessages -l <ISO_language_code>

        (i.e.) python manage.py makemessages -l es

### Adding new models

1. Define model name associated to translations

        class Meta:
          verbose_name = _('class_name')

### Adding new fields

1. Define field name associated to translations

        option -> verbose_name=_('field_name')

Common fields (Boolean, Char, Text, etc) can have this verbose name as the first parameter without include the verbose_name attribute name. 
The attribute name is a must for relations (ManyToMany, ForeignKeys, etc).

### Adding new model and field keys to .po files

1. Add keys to all .po files

        python manage.py makemessages

2. Translate each key for all existing languages

3. Compile new translations

        python manage.py compilemessages