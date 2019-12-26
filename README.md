# Cooperative social balance app 

## Running Backend

1. Create virtualenv using python3 (follow https://virtualenvwrapper.readthedocs.io/en/latest/install.html)


2. Activate the virtualenv

        workon {{VIRTUALENV_NAME}}

3. Install the requirements

        pip install -R requirements.txt

4. Create your postgres db
        sudo su - postgres psql
        CREATE DATABASE coobs;
        CREATE USER fiqus WITH PASSWORD 'fiquspass';
        ALTER ROLE fiqus SET client_encoding TO 'utf8';
        ALTER ROLE fiqus SET default_transaction_isolation TO 'read committed';
        ALTER ROLE fiqus SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE coobs TO fiqus;

5. Run database migrations

        python manage.py migrate 

6. Create a superuser

        python manage.py createsuperuser

7. Run the server

        python manage.py runserver

8. API now should be accessible in:

        http://localhost:8000/api/

## Running Frontend

1. Go to '/bscoop/frontend/' and run:

        npm install

2. Go to '/bscoop/frontend/landing' and run:

        npm install

3. Install eslint extension for vscode and configure settings file 


4. Go to '/bscoop/frontend/' and run:
        
        npm run dev

5. App core and landing page should be accesible on:

        http://localhost:8080/app
        http://localhost:8080/landing

## Frontend translations

### Adding new language

1. Go to '/bscoop/frontend/locales' and add the new language in 'langs.json' file

        key -> language short ISO code
        value -> language name

2. In the same folder add a new file with ISO code as name and '.json' extension

3. Add all existing translations for the new language.

### Adding new translation

1. Try to find if translation does not already exist.

2. Add new pair key/value in each translations file.
