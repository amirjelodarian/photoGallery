from graphql import middlewares
from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.photoForm, name='photo.form'),
    path('create', views.createPhoto, name='photo.create'),
    path('myGallery', views.photosByUserId, name='photo.myGallery'),
    path('category/<category>', views.photosByCategory, name='photo.category'),
    path('delete/<delete>', views.delete, name='photo.delete'),
    path('editForm/<edit>', views.editForm, name='photo.editForm'),
    path('edit/<edit>', views.edit, name='photo.edit'),
]
