# Cooperative social balance app 

## Running

1. Create virtualenv using python3 (follow https://virtualenvwrapper.readthedocs.io/en/latest/install.html)


2. Activate the virtualenv

        workon {{VIRTUALENV_NAME}}

3. Install the requirements

        pip install -R requirements.txt
        
4. Run database migrations

        python manage.py migrate 

5. Create a superuser

        python manage.py createsuperuser

6. Run the server

        python manage.py runserver

7. API now should be accessible in:

        http://localhost:8000/api/
