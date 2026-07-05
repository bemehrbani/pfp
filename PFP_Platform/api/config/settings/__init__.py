"""
Settings module for PFP Campaign Manager.
Loads appropriate settings based on DJANGO_SETTINGS_MODULE environment variable.
"""
import os

environment = os.environ.get('DJANGO_SETTINGS_MODULE', '')

if 'production' in environment:
    from .production import *
elif 'development' in environment:
    from .development import *
else:
    # Default to development for backward compatibility
    from .development import *