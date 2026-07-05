"""
URLs for Analytics app API.
"""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Dashboard statistics
    path('dashboard-stats/', views.DashboardStatsView.as_view(), name='dashboard_stats'),

    # Campaign analytics
    path('campaigns/<int:campaign_id>/', views.CampaignAnalyticsView.as_view(), name='campaign_analytics'),

    # System analytics (admin only)
    path('system/', views.SystemAnalyticsView.as_view(), name='system_analytics'),

    # General analytics endpoint
    path('', views.SystemAnalyticsView.as_view(), name='analytics_overview'),
]