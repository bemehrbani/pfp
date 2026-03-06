#!/bin/bash

# People for Peace Campaign Manager - Production Deployment Script
# This script deploys the application using Docker Compose for production

set -e

echo "========================================"
echo "People for Peace Campaign Manager Deployment"
echo "========================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed. Please install it and try again."
    exit 1
fi

# Load environment variables from .env.production if exists
ENV_FILE=".env.production"
if [ -f "$ENV_FILE" ]; then
    echo "Loading environment variables from $ENV_FILE"
    export $(cat "$ENV_FILE" | grep -v '^#' | xargs)
else
    echo "Warning: $ENV_FILE not found. Using default values and existing environment."
fi

# Validate required environment variables
required_vars=("SECRET_KEY" "DOMAIN_NAME" "ACME_EMAIL" "TELEGRAM_BOT_TOKEN" "ALLOWED_HOSTS" "CORS_ALLOWED_ORIGINS")
missing_vars=()
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "Error: Missing required environment variables:"
    for var in "${missing_vars[@]}"; do
        echo "  - $var"
    done
    echo ""
    echo "Please set them in $ENV_FILE or environment."
    exit 1
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p backend/logs backend/static backend/media
mkdir -p frontend/logs
mkdir -p telegram-bot/logs
mkdir -p infrastructure/traefik/letsencrypt
mkdir -p infrastructure/postgres/backups

# Set correct permissions for letsencrypt directory
chmod 600 infrastructure/traefik/letsencrypt 2>/dev/null || true

# Pull latest images (if any)
echo "Pulling latest base images..."
docker-compose -f docker-compose.production.yml pull

# Build and start services
echo "Building and starting Docker services..."
docker-compose -f docker-compose.production.yml up -d --build

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until docker-compose -f docker-compose.production.yml exec postgres pg_isready -U ${POSTGRES_USER:-pfp_user} > /dev/null 2>&1; do
    sleep 5
done

# Run database migrations
echo "Running database migrations..."
docker-compose -f docker-compose.production.yml exec backend python manage.py migrate

# Collect static files
echo "Collecting static files..."
docker-compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput

# Create superuser if not exists (optional)
echo "Checking superuser..."
docker-compose -f docker-compose.production.yml exec backend python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@peopleforpeace.org', '${ADMIN_PASSWORD:-admin123}');
    print('Superuser created: username=admin');
else:
    print('Superuser already exists');
"

# Restart backend to apply changes
echo "Restarting backend service..."
docker-compose -f docker-compose.production.yml restart backend

# Show deployment status
echo ""
echo "========================================"
echo "Deployment complete!"
echo "========================================"
echo ""
echo "Services deployed:"
echo "- PostgreSQL: healthy"
echo "- Redis: healthy"
echo "- Backend API: running"
echo "- Celery Worker: running"
echo "- Celery Beat: running"
echo "- Telegram Bot: running"
echo "- Frontend: running"
echo "- Reverse Proxy (Traefik): running"
echo ""
echo "Access the application:"
echo "- Frontend:      https://${DOMAIN_NAME}"
echo "- Backend API:   https://${DOMAIN_NAME}/api"
echo "- Admin Panel:   https://${DOMAIN_NAME}/admin"
echo "- API Docs:      https://${DOMAIN_NAME}/swagger/"
echo "- Telegram Webhook: https://${DOMAIN_NAME}/bot-webhook"
echo ""
echo "To view logs:"
echo "  docker-compose -f docker-compose.production.yml logs -f"
echo ""
echo "To stop the services:"
echo "  docker-compose -f docker-compose.production.yml down"
echo "========================================"