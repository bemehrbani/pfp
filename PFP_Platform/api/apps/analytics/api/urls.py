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

    # Lightweight first-party web analytics beacon (public) & summary (admin)
    path('pageview/', views.RecordPageViewView.as_view(), name='record_pageview'),
    path('web-summary/', views.WebAnalyticsSummaryView.as_view(), name='web_summary'),

    # General analytics endpoint
    path('', views.SystemAnalyticsView.as_view(), name='analytics_overview'),
]