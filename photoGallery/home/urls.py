from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.index, name='home'),
    path('posts', views.posts, name='posts'),
    path('author', views.author, name='author'),
]
