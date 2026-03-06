# People for Peace Campaign Manager - Makefile

.PHONY: help build up down logs migrate createsuperuser shell test clean

# Default target
help:
	@echo "People for Peace Campaign Manager - Development Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build        Build Docker images"
	@echo "  up           Start all services in background"
	@echo "  up-dev       Start services with logs in foreground"
	@echo "  down         Stop and remove all services"
	@echo "  logs         View logs from all services"
	@echo "  logs-backend View backend logs"
	@echo "  logs-frontend View frontend logs"
	@echo "  migrate      Run database migrations"
	@echo "  makemigrations Create new migrations"
	@echo "  createsuperuser Create admin user"
	@echo "  shell        Open Django shell"
	@echo "  test         Run backend tests"
	@echo "  test-frontend Run frontend tests"
	@echo "  clean        Remove all Docker containers, images, and volumes"
	@echo "  setup        Full development setup (run once)"
	@echo "  reset        Reset development database"

# Build Docker images
build:
	docker-compose build

# Start services in background
up:
	docker-compose up -d

# Start services in foreground (development)
up-dev:
	docker-compose up

# Stop services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# View backend logs
logs-backend:
	docker-compose logs -f backend

# View frontend logs
logs-frontend:
	docker-compose logs -f frontend

# Run database migrations
migrate:
	docker-compose exec backend python manage.py migrate

# Create migrations
makemigrations:
	docker-compose exec backend python manage.py makemigrations

# Create superuser
createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

# Open Django shell
shell:
	docker-compose exec backend python manage.py shell

# Run backend tests
test:
	docker-compose exec backend python manage.py test

# Run frontend tests (from frontend directory)
test-frontend:
	docker-compose exec frontend npm test

# Clean Docker environment
clean:
	docker-compose down -v
	docker system prune -af --volumes

# Full development setup
setup:
	@echo "Setting up development environment..."
	cp .env.example .env
	docker-compose up -d --build
	@echo "Waiting for services to start..."
	sleep 10
	docker-compose exec backend python manage.py migrate
	docker-compose exec backend python manage.py createsuperuser
	@echo "Setup complete! Access:"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend API: http://localhost:8000"
	@echo "  Admin: http://localhost:8000/admin"

# Reset development database
reset:
	docker-compose down -v
	docker-compose up -d postgres redis
	@echo "Waiting for PostgreSQL..."
	sleep 5
	docker-compose exec postgres psql -U pfp_user -c "DROP DATABASE IF EXISTS pfp_campaign;"
	docker-compose exec postgres psql -U pfp_user -c "CREATE DATABASE pfp_campaign;"
	docker-compose up -d
	sleep 5
	docker-compose exec backend python manage.py migrate
	docker-compose exec backend python manage.py createsuperuser
	@echo "Database reset complete"

# Collect static files
collectstatic:
	docker-compose exec backend python manage.py collectstatic --noinput

# Run Celery worker
celery-worker:
	docker-compose exec celery celery -A config worker --loglevel=info

# Run Celery beat
celery-beat:
	docker-compose exec celery-beat celery -A config beat --loglevel=info

# Start Telegram bot in polling mode
telegram-bot:
	docker-compose exec telegram-bot python bot.py --mode polling

# Check service status
status:
	docker-compose ps