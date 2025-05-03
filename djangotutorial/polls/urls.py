from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_meeting, name='create_meeting'),
    path('meetings/', views.list_meetings, name='list_meetings'),
    path('meeting/<int:meeting_id>/', views.meeting_detail, name='meeting_detail'),
    path('edit/<int:meeting_id>/', views.edit_meeting, name='edit_meeting'),
    path('delete/<int:meeting_id>/', views.delete_meeting, name='delete_meeting'),
    path('report/', views.meeting_report, name='meeting_report'),
]