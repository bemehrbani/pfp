# People for Peace Campaign Program Manager

A comprehensive system for managing "People for Peace" campaigns, helping Campaign Managers create, run, analyze, and expand campaigns using Telegram BOT, Groups, and Channels. The system facilitates attracting, organizing, cooperating, and crowdsourcing campaign tasks to achieve campaign goals.

## Project Status: Phase 2 - Campaign Management ✅

This project is being implemented in phases according to the implementation plan. Currently, Phase 2 (Campaign Management) is complete. The system includes comprehensive campaign and task management, Telegram bot integration, analytics, and production deployment configuration.

## Features

### Core Features (Planned)
- **Campaign Management**: Create, manage, and track campaigns with member/activity goals
- **Task Crowdsourcing**: Social media actions that volunteers can claim and complete
- **Telegram Bot Integration**: Interactive bot for volunteer engagement
- **Analytics Dashboard**: Track campaign metrics and performance
- **Twitter Storm Support**: Coordinate manual Twitter operations
- **Role-based Access**: Admin, Campaign Manager, and Volunteer roles
- **Points System**: Reward volunteers for completed tasks

## Technology Stack

### Backend
- **Django 4.2** + **Django REST Framework** - API and business logic
- **PostgreSQL** - Primary database with JSONB support
- **Redis** - Caching and Celery broker
- **Celery** - Background task processing
- **Django Channels** - WebSocket support for real-time updates
- **JWT Authentication** - Secure API authentication
- **python-telegram-bot** - Telegram bot integration

### Frontend
- **React 18** + **TypeScript** - User interface
- **React Router** - Client-side routing
- **TanStack Query** - Data fetching and state management
- **Tailwind CSS** - Styling and design system
- **Axios** - HTTP client

### Infrastructure
- **Docker** + **Docker Compose** - Containerization and orchestration
- **Nginx** - Reverse proxy and static file serving
- **Gunicorn** - WSGI server for Django

## Project Structure

```
pfp-campaign-manager/
├── backend/                 # Django backend
│   ├── apps/               # Django applications
│   │   ├── users/          # Authentication and user profiles
│   │   ├── campaigns/      # Campaign management
│   │   ├── tasks/          # Task management
│   │   ├── analytics/      # Analytics engine
│   │   └── telegram/       # Telegram bot integration
│   ├── config/             # Django settings
│   ├── manage.py
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/          # Page components
│   │   ├── components/     # Reusable UI components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── utils/          # Utility functions
│   │   └── api/            # API client setup
│   ├── public/             # Static assets
│   ├── package.json
│   └── Dockerfile
├── telegram-bot/           # Telegram bot service (to be implemented)
├── infrastructure/         # Deployment configurations
├── docker-compose.yml      # Development environment
├── requirements.txt        # Python dependencies
└── .env.example            # Environment variables template
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### Quick Start with Docker (Recommended)

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd pfp-campaign-manager
   cp .env.example .env
   # Edit .env if needed (defaults work for development)
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Apply database migrations**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Django Admin: http://localhost:8000/admin
   - API Documentation: http://localhost:8000/swagger/

### Manual Development Setup

#### Backend Setup
1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp ../.env.example ../.env
   # Edit .env with your configuration
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

#### Frontend Setup
1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

## API Documentation

Once the backend is running, access the interactive API documentation:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Database Models

### Core Models
1. **User**: Custom user model with roles (admin/campaign_manager/volunteer) and Telegram linking
2. **Campaign**: Campaigns with goals (members/activities), status, and Twitter storm support
3. **Task**: Social media actions with assignment types and points
4. **TaskAssignment**: Volunteer assignments with completion status and proof
5. **ActivityLog**: User actions for analytics
6. **TelegramSession**: Bot conversation state management

## Development

### Running Tests
```bash
# Backend tests
docker-compose exec backend python manage.py test

# Frontend tests (from frontend directory)
npm test
```

### Code Quality
```bash
# Backend linting
docker-compose exec backend python -m flake8 .

# Frontend linting
cd frontend && npm run lint
```

### Database Management
```bash
# Create migrations
docker-compose exec backend python manage.py makemigrations

# Apply migrations
docker-compose exec backend python manage.py migrate

# Reset database (development only)
docker-compose down -v
docker-compose up -d postgres
docker-compose exec backend python manage.py migrate
```

## Deployment

### Production Deployment with Docker Compose

The project includes production-ready Docker configuration with Traefik reverse proxy for automatic SSL certificate management.

1. **Set up production environment variables**
   ```bash
   cp .env.production.example .env.production
   # Edit .env.production with your production values
   # Required variables: SECRET_KEY, DOMAIN_NAME, ACME_EMAIL, TELEGRAM_BOT_TOKEN
   ```

2. **Run the deployment script**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

   The deployment script will:
   - Validate environment variables
   - Build production Docker images
   - Start all services (PostgreSQL, Redis, Backend, Celery, Telegram Bot, Frontend, Traefik)
   - Run database migrations
   - Collect static files
   - Create admin user (if not exists)

3. **Access the application**
   - Frontend: `https://yourdomain.com`
   - Backend API: `https://yourdomain.com/api`
   - Admin Panel: `https://yourdomain.com/admin`
   - API Documentation: `https://yourdomain.com/swagger/`
   - Telegram Webhook: `https://yourdomain.com/bot-webhook`

4. **Management commands**
   ```bash
   # View logs
   docker-compose -f docker-compose.production.yml logs -f

   # Stop services
   docker-compose -f docker-compose.production.yml down

   # Update deployment (after code changes)
   docker-compose -f docker-compose.production.yml up -d --build
   ```

### Manual Production Deployment

If you prefer to run commands manually:

```bash
# Build and start services
docker-compose -f docker-compose.production.yml up -d --build

# Run migrations
docker-compose -f docker-compose.production.yml exec backend python manage.py migrate

# Collect static files
docker-compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput

# Create superuser (optional)
docker-compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

### Environment Variables Reference

See `.env.production.example` for all available environment variables. Key variables:

- `SECRET_KEY`: Django secret key (generate with `openssl rand -base64 32`)
- `DOMAIN_NAME`: Your domain name (e.g., `campaign.peopleforpeace.org`)
- `ACME_EMAIL`: Email for Let's Encrypt certificate notifications
- `TELEGRAM_BOT_TOKEN`: Telegram bot token from @BotFather
- `TELEGRAM_WEBHOOK_URL`: Full webhook URL (e.g., `https://yourdomain.com/bot-webhook`)
- `POSTGRES_PASSWORD`: Secure password for PostgreSQL
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of CORS origins

### SSL Certificates

Traefik automatically obtains and renews SSL certificates from Let's Encrypt. Certificates are stored in `infrastructure/traefik/letsencrypt/`.

### Backup and Recovery

Regular backups are recommended. The PostgreSQL data volume is persisted in Docker volume `postgres_data`. You can create backups using:

```bash
docker-compose -f docker-compose.production.yml exec postgres pg_dump -U pfp_user pfp_campaign > backup_$(date +%Y%m%d).sql
```

## Implementation Phases

1. **Phase 1: Foundation Setup** ✅ COMPLETED
   - Django project setup with 5 modular apps
   - PostgreSQL with JSONB support + Redis for caching/Celery
   - JWT authentication with custom User model (roles: admin/manager/volunteer)
   - Comprehensive REST API endpoints for all core functionality
   - Signal handlers for automated logging and statistics
   - Permission classes for role-based access control

2. **Phase 2: Campaign Management** ✅ COMPLETED
   - Campaign CRUD operations with goals, Twitter storm support, statistics
   - Task management with social media actions, assignment logic, verification workflow
   - Volunteer enrollment and points system with level progression
   - Analytics dashboard with charts and recent activity tracking
   - Telegram bot integration with handlers for campaigns, tasks, profile, leaderboard
   - Frontend interface with React + TypeScript + Tailwind CSS
   - Production deployment configuration with Docker Compose + Traefik + SSL

3. **Phase 3: Telegram Bot Integration** ✅ COMPLETED
   - Bot skeleton with polling/webhook modes
   - Command handlers for campaigns, tasks, profile, leaderboard
   - Registration flow for new Telegram users
   - Conversation states for task completion proof submission
   - Database models for session management and message auditing
   - Integration with Django models and API endpoints

4. **Phase 4: Volunteer Experience** ✅ COMPLETED
   - Volunteer web portal with dashboard, campaigns, and tasks
   - Notification system (integrated with Telegram)
   - Points and rewards system with level progression
   - Responsive design with Tailwind CSS
   - Real-time updates via WebSocket (Channels)

5. **Phase 5: Analytics & Reporting** ✅ COMPLETED
   - Analytics data collection via ActivityLog model
   - Dashboard with charts for campaign metrics and system analytics
   - Real-time updates using Django Channels
   - Role-based access to analytics data

6. **Phase 6: Twitter Storm Support** ⏳ PLANNED
   - Twitter campaign planning tools
   - Coordination tools for manual Twitter operations
   - Schedule management for Twitter storms
   - Integration with campaign task system

7. **Phase 7: Deployment & Polish** ✅ COMPLETED
   - Production Docker configuration with Traefik reverse proxy
   - Automatic SSL certificate management with Let's Encrypt
   - Comprehensive test suite for all Django apps
   - Deployment scripts for automated production deployment
   - Performance optimization and security hardening

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is proprietary software developed for People for Peace campaigns.

## Contact

For questions or support, contact the development team at dev@peopleforpeace.org