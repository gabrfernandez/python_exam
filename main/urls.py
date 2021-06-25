from django.urls import path
from main import views

urlpatterns=[
    path("", views.show_login_reg_page),
    path("users", views.register_form),
    path("dashboard", views.show_dashboard),
    path("login", views.login_form),
    path("logout", views.logout),
    path("createjob", views.create_job),
    path('create_job_form', views.create_job_form),
    path('jobs/<int:job_id>' , views.job_profile), 
    path('jobs/edit/<int:job_id>' , views.edit_job_page),
    path('jobs/edit/<int:job_id>/update', views.update),
    path('jobs/<int:job_id>/delete', views.delete),
]