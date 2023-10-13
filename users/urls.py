from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from users.views import *

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/reset_password/', reset_password, name='reset_password'),
    path('register/verify_email/', TemplateView.as_view(template_name='users/verify.html'), name='verify_email'),
    path('register/success/', TemplateView.as_view(template_name='users/success_verify.html'), name='success_verify'),
    path('register/failure/', TemplateView.as_view(template_name='users/failure_verify.html'), name='failure_verify'),
    path('activate/<uidb64>[0-9A-Za-z]+<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}', activate, name='activate'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('to_active/<int:pk>', toggle_active, name='toggle_active')
]
