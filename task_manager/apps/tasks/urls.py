from django.urls import path

from task_manager.apps.tasks import views

urlpatterns = [
    path('', views.TasksView.as_view(), name='tasks'),
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path('<int:pk>/update/', views.UpdateTaskView.as_view(), name='update_task'),
    path('<int:pk>/delete/', views.DeleteTaskView.as_view(), name='delete_task'),
    path('<int:pk>/', views.DetailTaskView.as_view(), name='task_detail'),
]
