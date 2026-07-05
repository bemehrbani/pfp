"""
URLs for Tasks app API.
"""
from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # Task management
    path('', views.TaskListView.as_view(), name='task_list'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),

    # Available tasks for volunteers
    path('available/', views.AvailableTasksView.as_view(), name='available_tasks'),

    # Task assignment
    path('assign/', views.TaskAssignmentView.as_view(), name='task_assign'),
    path('my-assignments/', views.MyTaskAssignmentsView.as_view(), name='my_assignments'),

    # Task completion and verification
    path('assignments/<int:assignment_id>/complete/', views.TaskCompletionView.as_view(), name='task_complete'),
    path('assignments/<int:assignment_id>/verify/', views.TaskVerificationView.as_view(), name='task_verify'),
]