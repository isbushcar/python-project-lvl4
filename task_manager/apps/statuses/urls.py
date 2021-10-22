from django.urls import path

from task_manager.apps.statuses import views

urlpatterns = [
    path('statuses/', views.StatusesView.as_view(), name='statuses'),
    path('statuses/create/', views.CreateStatusView.as_view(), name='create_status'),
    path('statuses/<int:pk>/update/', views.UpdateStatusView.as_view(), name='update_status'),
    path('statuses/<int:pk>/delete/', views.DeleteStatusView.as_view(), name='delete_status'),
]
