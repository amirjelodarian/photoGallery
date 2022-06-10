from unittest import loader
from django.http import HttpResponse
from django.shortcuts import redirect, render
from sqlalchemy import null
from urllib3 import HTTPResponse
from category.models import Category
from photo.models import Photo

import user

# Create your views here.

def index(request):
    photos = Photo.objects.all()
    categories = Category.objects.all()
    return render(request, 'index.html', {'photos': photos, 'categories': categories})

def posts(request): 
    return render(request, "post.html")

def author(request):
    return render(request, "author.html")
