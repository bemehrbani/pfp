"""
URLs for Campaigns app API.
"""
from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    # Campaign management
    path('', views.CampaignListView.as_view(), name='campaign_list'),
    path('<int:pk>/', views.CampaignDetailView.as_view(), name='campaign_detail'),
    path('<int:pk>/join/', views.CampaignJoinView.as_view(), name='campaign_join'),
    path('<int:pk>/volunteers/', views.CampaignVolunteersView.as_view(), name='campaign_volunteers'),
    path('<int:pk>/updates/', views.CampaignUpdatesView.as_view(), name='campaign_updates'),
    path('<int:pk>/stats/', views.CampaignStatsView.as_view(), name='campaign_stats'),

    # User-specific campaigns
    path('my-campaigns/', views.MyCampaignsView.as_view(), name='my_campaigns'),
    path('search/', views.CampaignSearchView.as_view(), name='campaign_search'),
]