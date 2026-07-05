#!/bin/bash

# People for Peace Campaign Manager - Development Setup Script
# This script sets up the development environment using Docker Compose

set -e

echo "========================================"
echo "People for Peace Campaign Manager Setup"
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

# Load environment variables
if [ -f .env ]; then
    echo "Loading environment variables from .env"
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Warning: .env file not found. Using default values."
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p backend/logs backend/static backend/media

# Build and start services
echo "Building and starting Docker services..."
docker-compose up -d --build

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until docker-compose exec postgres pg_isready -U pfp_user > /dev/null 2>&1; do
    sleep 2
done

# Run database migrations
echo "Running database migrations..."
docker-compose exec backend python manage.py migrate

# Create superuser if not exists
echo "Creating superuser..."
docker-compose exec backend python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@peopleforpeace.org', 'admin123');
    print('Superuser created: username=admin, password=admin123');
else:
    print('Superuser already exists');
"

# Collect static files
echo "Collecting static files..."
docker-compose exec backend python manage.py collectstatic --noinput

# Create default data (optional)
echo "Creating default data..."
docker-compose exec backend python manage.py shell -c "
from apps.campaigns.models import Campaign;
from apps.users.models import User;
if Campaign.objects.count() == 0:
    admin = User.objects.get(username='admin');
    campaign = Campaign.objects.create(
        name='Welcome Campaign',
        description='Welcome to People for Peace! This is a sample campaign.',
        short_description='Sample welcome campaign',
        created_by=admin,
        target_members=100,
        target_activities=500
    );
    campaign.managers.add(admin);
    print('Sample campaign created');
else:
    print('Campaigns already exist');
"

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Access the following services:"
echo "- Frontend:      http://localhost:3000"
echo "- Backend API:   http://localhost:8000"
echo "- Admin Panel:   http://localhost:8000/admin"
echo "- API Docs:      http://localhost:8000/swagger/"
echo ""
echo "Default superuser credentials:"
echo "- Username: admin"
echo "- Password: admin123"
echo ""
echo "To stop the services:"
echo "  docker-compose down"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo "========================================"