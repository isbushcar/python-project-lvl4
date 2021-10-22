from django.urls import path

from task_manager.apps.labels import views

urlpatterns = [
    path('labels/', views.LabelsView.as_view(), name='labels'),
    path('labels/create/', views.CreateLabelView.as_view(), name='create_label'),
    path('labels/<int:pk>/update/', views.UpdateLabelView.as_view(), name='update_label'),
    path('labels/<int:pk>/delete/', views.DeleteLabelView.as_view(), name='delete_label'),
]
