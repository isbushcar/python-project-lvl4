from django.urls import path

from task_manager.apps.labels import views

urlpatterns = [
    path('', views.LabelsView.as_view(), name='labels'),
    path('create/', views.CreateLabelView.as_view(), name='create_label'),
    path('<int:pk>/update/', views.UpdateLabelView.as_view(), name='update_label'),
    path('<int:pk>/delete/', views.DeleteLabelView.as_view(), name='delete_label'),
]
