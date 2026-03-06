"""
Health check views for monitoring and load balancers.
"""
from django.http import JsonResponse
from django.db import connection
from redis import Redis
from django.conf import settings
import logging
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def health_check(request):
    """
    Comprehensive health check endpoint.
    Returns 200 if all systems are operational, 503 otherwise.
    """
    health_status = {
        'status': 'healthy',
        'services': {}
    }
    overall_healthy = True

    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['services']['database'] = 'healthy'
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status['services']['database'] = 'unhealthy'
        overall_healthy = False

    # Redis check
    try:
        redis_client = Redis.from_url(settings.REDIS_URL)
        redis_client.ping()
        health_status['services']['redis'] = 'healthy'
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        health_status['services']['redis'] = 'unhealthy'
        overall_healthy = False

    # Celery check (basic - just check if we can connect to broker)
    try:
        # Simple check - try to import Celery and get app
        from config.celery import app as celery_app
        # Try to get the result backend connection
        celery_app.backend.ensure_connection()
        health_status['services']['celery'] = 'healthy'
    except Exception as e:
        logger.error(f"Celery health check failed: {e}")
        health_status['services']['celery'] = 'unhealthy'
        # Don't fail overall for Celery - it's not critical for basic functionality
        # overall_healthy = False

    # Application status
    health_status['services']['application'] = 'healthy'
    health_status['version'] = '1.0.0'
    health_status['environment'] = 'production' if not settings.DEBUG else 'development'

    if not overall_healthy:
        health_status['status'] = 'unhealthy'
        return Response(health_status, status=503)

    return Response(health_status)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def simple_health(request):
    """
    Simple health check for load balancers.
    Returns 200 with minimal response.
    """
    return Response({'status': 'ok'}, status=200)