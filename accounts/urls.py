from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'),
         name='change_password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),

]
