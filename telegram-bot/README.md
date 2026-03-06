# Telegram Bot for People for Peace Campaign Manager

The Telegram bot provides volunteer interaction interface for the campaign system. Volunteers can register, browse campaigns, claim tasks, submit proof, and track progress through the bot.

## Features

- **Volunteer Registration**: New users can register via Telegram
- **Campaign Browsing**: List and join available campaigns
- **Task Management**: Claim, complete, and submit proof for tasks
- **Progress Tracking**: Check points, level, and leaderboard position
- **Real-time Notifications**: Get notified about new tasks and campaign updates
- **Interactive Menus**: Easy-to-use inline keyboards and conversation flows

## Architecture

The bot is built using:
- **python-telegram-bot** (v20+) - Modern async Telegram Bot API wrapper
- **Django ORM** - Direct database access for user and campaign data
- **Redis** - Conversation state management (optional)
- **Webhooks** - Production deployment with Django backend integration

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL database (shared with Django backend)
- Redis (for state management)
- Telegram Bot Token from [@BotFather](https://t.me/botfather)

### Installation

1. **Copy environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your bot token and database settings
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Django environment**
   Ensure the Django backend is running and database migrations are applied.

### Running the Bot

#### Development (Polling Mode)
```bash
python bot.py --mode polling
```

#### Production (Webhook Mode)
```bash
python bot.py --mode webhook --webhook-url https://your-domain.com
```

### Docker
```bash
docker build -t pfp-telegram-bot .
docker run -p 8443:8443 --env-file .env pfp-telegram-bot
```

## Bot Commands

- `/start` - Start conversation and show welcome message
- `/help` - Show help information
- `/campaigns` - List available campaigns
- `/tasks` - Show tasks available for claiming
- `/mytasks` - Show your assigned tasks
- `/profile` - Show your profile and points
- `/leaderboard` - Show top volunteers
- `/settings` - Configure notification preferences

## Conversation States

The bot uses conversation states for multi-step interactions:
1. **Registration**: Collect email and profile information
2. **Task Completion**: Submit proof for completed tasks
3. **Campaign Join**: Select and join campaigns
4. **Feedback**: Collect volunteer feedback

## Integration with Django Backend

The bot integrates with the Django backend through:
- **Database Models**: Direct access to User, Campaign, Task models
- **REST API**: API calls for complex operations
- **WebSocket**: Real-time notifications (optional)
- **Shared Authentication**: JWT tokens for API access

## Development

### Adding New Handlers

1. Create handler module in `handlers/` directory
2. Register handler in `bot.py` `_init_handlers()` method
3. Add command documentation to `help_command`

### Adding New Keyboards

1. Create keyboard functions in `keyboards/` directory
2. Import and use in handlers
3. Follow consistent callback data patterns

### Testing

```bash
# Run unit tests
python -m pytest tests/

# Test with Telegram API (requires bot token)
python test_bot.py
```

## Deployment

### Webhook Setup

1. **Configure webhook URL** in `.env` file
2. **Set up SSL certificate** (Let's Encrypt recommended)
3. **Configure reverse proxy** (Nginx) to forward requests to bot
4. **Set up process manager** (systemd/supervisor) for bot service

### Monitoring

- **Logs**: Check bot logs for errors and user interactions
- **Metrics**: Track user engagement and task completion rates
- **Alerts**: Set up alerts for bot downtime or errors

## Security Considerations

- **Token Security**: Keep bot token secret, never commit to version control
- **User Data**: Protect volunteer personal information
- **Input Validation**: Validate all user input to prevent abuse
- **Rate Limiting**: Implement rate limiting for API calls
- **Admin Controls**: Restrict sensitive commands to admin users

## Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check bot token in `.env` file
   - Verify internet connectivity
   - Check for API rate limits

2. **Database connection errors**
   - Verify database credentials
   - Check if Django backend is running
   - Ensure database migrations are applied

3. **Webhook issues**
   - Verify SSL certificate is valid
   - Check webhook URL is accessible
   - Verify port is open and not blocked by firewall

### Logs

Enable debug logging by setting `BOT_LOGGING_LEVEL=DEBUG` in `.env` file.

## Contributing

1. Follow the existing code style and patterns
2. Add tests for new functionality
3. Update documentation for new features
4. Submit pull requests for review

## License

Proprietary software - People for Peace Campaign Manager