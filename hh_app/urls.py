from django.urls import path
from . import views

urlpatterns = [
    path('resumes/', views.ResumeListView.as_view(), name='resume-list'),
    path('resumes/<int:resume_id>/status/', views.ResumeStatusUpdateView.as_view(), name='resume-status-update'),
]