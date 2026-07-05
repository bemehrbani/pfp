"""
Management command to resolve a Telegram channel username to its numeric ID.

Usage:
    python manage.py resolve_channel_id @people4peace
    python manage.py resolve_channel_id people4peace
    python manage.py resolve_channel_id @people4peace --set-campaign 1

The resolved ID can then be set on Campaign.telegram_channel_id via Django admin
or directly with the --set-campaign flag.
"""
import asyncio
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Resolve a Telegram channel/group username to its numeric chat ID'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
            help='Telegram channel username (with or without @)',
        )
        parser.add_argument(
            '--set-campaign',
            type=int,
            default=None,
            help='Campaign ID to set the resolved channel_id on',
        )
        parser.add_argument(
            '--set-all-active',
            action='store_true',
            help='Set the resolved channel_id on ALL active campaigns',
        )

    def handle(self, *args, **options):
        username = options['username'].lstrip('@')
        token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '') or os.environ.get('TELEGRAM_BOT_TOKEN', '')

        if not token:
            raise CommandError(
                'TELEGRAM_BOT_TOKEN not found in settings or environment. '
                'Set it in .env or pass via environment variable.'
            )

        # Resolve channel ID using the Telegram Bot API
        chat_id = asyncio.run(self._resolve_chat_id(token, username))

        if chat_id is None:
            raise CommandError(
                f'Could not resolve @{username}. Make sure:\n'
                f'  1. The channel/group exists\n'
                f'  2. The bot (@peopleforpeacebot) is an admin of the channel\n'
                f'  3. The username is spelled correctly'
            )

        self.stdout.write(self.style.SUCCESS(f'Resolved @{username} → {chat_id}'))

        # Optionally set on campaign(s)
        if options['set_campaign']:
            self._set_on_campaign(options['set_campaign'], chat_id)
        elif options['set_all_active']:
            self._set_on_all_active(chat_id)
        else:
            self.stdout.write(
                f'\nTo set this on a campaign, run:\n'
                f'  python manage.py resolve_channel_id @{username} --set-campaign <ID>\n'
                f'  python manage.py resolve_channel_id @{username} --set-all-active'
            )

    async def _resolve_chat_id(self, token: str, username: str) -> int | None:
        """Use Telegram Bot API getChat to resolve username to numeric ID."""
        import httpx

        url = f'https://api.telegram.org/bot{token}/getChat'
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json={'chat_id': f'@{username}'})
                data = response.json()

                if data.get('ok'):
                    chat = data['result']
                    chat_id = chat['id']
                    chat_type = chat.get('type', 'unknown')
                    title = chat.get('title', username)
                    self.stdout.write(f'  Type: {chat_type}')
                    self.stdout.write(f'  Title: {title}')
                    self.stdout.write(f'  ID: {chat_id}')
                    return chat_id
                else:
                    self.stderr.write(self.style.ERROR(
                        f'Telegram API error: {data.get("description", "Unknown error")}'
                    ))
                    return None
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f'Request failed: {exc}'))
                return None

    def _set_on_campaign(self, campaign_id: int, chat_id: int):
        """Set telegram_channel_id on a specific campaign."""
        from apps.campaigns.models import Campaign

        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            raise CommandError(f'Campaign {campaign_id} not found')

        campaign.telegram_channel_id = chat_id
        campaign.save(update_fields=['telegram_channel_id'])
        self.stdout.write(self.style.SUCCESS(
            f'✅ Set telegram_channel_id={chat_id} on campaign "{campaign.name}" (ID={campaign.id})'
        ))

    def _set_on_all_active(self, chat_id: int):
        """Set telegram_channel_id on all active campaigns."""
        from apps.campaigns.models import Campaign

        active = Campaign.objects.filter(status=Campaign.Status.ACTIVE)
        count = active.update(telegram_channel_id=chat_id)
        self.stdout.write(self.style.SUCCESS(
            f'✅ Set telegram_channel_id={chat_id} on {count} active campaign(s)'
        ))
