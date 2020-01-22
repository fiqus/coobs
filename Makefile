.PHONY: server frontend migration test

server:
	@python manage.py runserver

frontend:
	@cd frontend && npm run dev

frontend-install:
	@cd frontend/landing && npm install
	@cd frontend && npm install && npm run build

migration:
	@python manage.py migrate

test:
	@echo "TODO"
