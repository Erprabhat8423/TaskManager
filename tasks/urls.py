from django.urls import path
from .views import (
    RegisterView, LoginView, TaskCreateView, TaskListView, TaskDetailView,
    AddRemoveTaskMemberView, TaskMemberListView, CommentCreateView, TaskStatusUpdateView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/members/', TaskMemberListView.as_view(), name='task-members'),
    path('tasks/<int:pk>/add_member/', AddRemoveTaskMemberView.as_view(), name='add-task-member'),
    path('tasks/<int:pk>/remove_member/', AddRemoveTaskMemberView.as_view(), name='remove-task-member'),
    path('tasks/<int:task_pk>/comments/', CommentCreateView.as_view(), name='task-comment-create'),
    path('tasks/<int:pk>/status/', TaskStatusUpdateView.as_view(), name='task-status-update'),
]
