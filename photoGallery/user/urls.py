from . import views
from django.urls import include, path

urlpatterns = [
    path('register', views.registerForm, name='registerForm'),
    path('register/create', views.createUser, name='user.create'),
    path('login', views.loginForm, name='loginForm'),
    path('login/create', views.loginUser, name='user.login'),
    path('logout', views.logOut, name='user.logout')
]
