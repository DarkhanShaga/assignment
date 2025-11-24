from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list_create, name='user-list-create'),
    path('users/<int:user_id>/', views.user_detail, name='user-detail'),
    path('caregivers/', views.caregiver_list_create, name='caregiver-list-create'),
    path('caregivers/<int:caregiver_user_id>/', views.caregiver_detail, name='caregiver-detail'),
    path('members/', views.member_list_create, name='member-list-create'),
    path('members/<int:member_user_id>/', views.member_detail, name='member-detail'),
    path('addresses/', views.address_list_create, name='address-list-create'),
    path('addresses/<int:member_user_id>/', views.address_detail, name='address-detail'),
    path('jobs/', views.job_list_create, name='job-list-create'),
    path('jobs/<int:job_id>/', views.job_detail, name='job-detail'),
    path('job-applications/', views.job_application_list_create, name='job-application-list-create'),
    path('job-applications/<int:caregiver_user_id>/<int:job_id>/', views.job_application_detail, name='job-application-detail'),
    path('appointments/', views.appointment_list_create, name='appointment-list-create'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment-detail'),
]

