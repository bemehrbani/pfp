"""
URLs for Campaigns app API.
"""
from django.urls import path
from . import views
from . import storm_views

app_name = 'campaigns'

urlpatterns = [
    # Campaign management
    path('', views.CampaignListView.as_view(), name='campaign_list'),
    path('<int:pk>/', views.CampaignDetailView.as_view(), name='campaign_detail'),
    path('<int:pk>/join/', views.CampaignJoinView.as_view(), name='campaign_join'),
    path('<int:pk>/volunteers/', views.CampaignVolunteersView.as_view(), name='campaign_volunteers'),
    path('<int:pk>/updates/', views.CampaignUpdatesView.as_view(), name='campaign_updates'),
    path('<int:pk>/stats/', views.CampaignStatsView.as_view(), name='campaign_stats'),

    # Twitter Storm management
    path('<int:campaign_pk>/storms/', storm_views.StormListCreateView.as_view(), name='storm_list'),
    path('storms/<int:pk>/', storm_views.StormDetailView.as_view(), name='storm_detail'),
    path('storms/<int:pk>/activate/', storm_views.StormActivateView.as_view(), name='storm_activate'),
    path('storms/<int:pk>/cancel/', storm_views.StormCancelView.as_view(), name='storm_cancel'),
    path('storms/<int:pk>/participants/', storm_views.StormParticipantsView.as_view(), name='storm_participants'),

    # User-specific campaigns
    path('my-campaigns/', views.MyCampaignsView.as_view(), name='my_campaigns'),
    path('search/', views.CampaignSearchView.as_view(), name='campaign_search'),

    # Public stats (no auth)
    path('<int:pk>/public-stats/', views.PublicCampaignStatsView.as_view(), name='public_campaign_stats'),
]