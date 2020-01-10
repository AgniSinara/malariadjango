from django.urls import path

from .views import *


urlpatterns = [
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('me', my_profile, name='my_profile')
]
