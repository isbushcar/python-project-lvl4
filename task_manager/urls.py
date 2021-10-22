"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from task_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='main_page'),
    path('users/', views.UsersView.as_view(), name='users_list'),
    path('users/create/', views.CreateUserView.as_view(), name='create_user'),
    path('users/<int:pk>/update/', views.UpdateUserView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete_user'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('statuses/', include('task_manager.apps.statuses.urls')),
    path('tasks/', views.TasksView.as_view(), name='tasks'),
    path('tasks/create/', views.CreateTaskView.as_view(), name='create_task'),
    path('tasks/<int:pk>/update/', views.UpdateTaskView.as_view(), name='update_task'),
    path('tasks/<int:pk>/delete/', views.DeleteTaskView.as_view(), name='delete_task'),
    path('tasks/<int:pk>/', views.DetailTaskView.as_view(), name='task_detail'),
    path('labels/', views.LabelsView.as_view(), name='labels'),
    path('labels/create/', views.CreateLabelView.as_view(), name='create_label'),
    path('labels/<int:pk>/update/', views.UpdateLabelView.as_view(), name='update_label'),
    path('labels/<int:pk>/delete/', views.DeleteLabelView.as_view(), name='delete_label'),
]
