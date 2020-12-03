.PHONY: server frontend install-frontend install-requirements migration clean reset-db test

server:
	@python manage.py runserver

frontend:
	@cd frontend && npm run build-dev && npm run start

install-frontend:
	@cd frontend && npm install
	@cd frontend/landing && npm install

install-requirements:
	@pip install -r requirements.txt

migration:
	@python manage.py migrate

clean:
	@rm -rf frontend/dist frontend/node_modules frontend/landing/node_modules

reset-db:
	@sudo -iu postgres bash -c "psql -c 'DROP DATABASE IF EXISTS coobs;'"
	@sudo -iu postgres bash -c "psql -c 'CREATE DATABASE coobs;'"
	@sudo -iu postgres bash -c "psql -c 'GRANT ALL PRIVILEGES ON DATABASE coobs TO coobs;'"
	@sudo -iu postgres bash -c "psql -c 'ALTER USER coobs CREATEDB;'"
	@echo "\033[0;32mDB reset done! => Running migrations.."
	@$(MAKE) -s migration
	@echo "\033[0;32mMigrations done! => Creating superuser.."
	@python manage.py createsuperuser

test:
	@echo "\033[0;31mRunning tests!\033[0m"
	@python manage.py test
