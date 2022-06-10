import os
from unicodedata import category, name
import uuid
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from sqlalchemy import null
from photo.context_processors import userOwner
import user
from photo.models import Photo
from user.models import User
from category.models import Category
from django.core.validators import validate_email
from django.core.files.storage import FileSystemStorage
# Create your views here.

def photoForm(request):
    categories = Category.objects.all()
    if not user.views.loggedIn(request):
        return redirect('home')
    return render(request, 'createPhoto.html', {'categories': categories})

def createPhoto(request):
    categories = Category.objects.all()
    try:
        if request.method == 'POST':
            if validatePhotoForm(request) == True:
                photo = uploadPhoto(request)
                photoNew = Photo.objects.create(title= request.POST['title'] ,description= request.POST['description'], user=User.objects.get(id= request.session['user_id']), path='/media/'+photo)
                addCategory(request, photoNew)
                return photosByUserId(request)
            else:
                return render(request, 'createPhoto.html', {'error': validatePhotoForm(request), 'categories': categories})
    except:
        return redirect('photo')
    
def addCategory(request, photo):
     for category in request.POST.getlist('category'):
        if not Category.objects.filter(name= category).exists():
            category_ = Category.objects.create(name= category)
        else:
            category_ = Category.objects.get(name= category)
        photo.category.add(category_)

def removeCategory(photo):
    for category in list(photo.category.all()):
        photo.category.remove(category)
def uploadPhoto(request):
    if request.method == 'POST' and request.FILES['file']:
        try:
            upload = request.FILES['file']
            fss = FileSystemStorage()
            rndText = str(uuid.uuid4().hex)
            base = os.path.basename(upload.name)
            extension = os.path.splitext(base)[1]
            fileName = rndText + extension
            while (Photo.objects.filter(path= fileName).exists()):
                rndText = str(uuid.uuid4().hex)
                fileName = rndText + extension
            fss.save(fileName, upload)
            return fileName
        except:
            redirect('photo.form', {'error': 'something wrong in photo uploading!'})
    else:
        return render(request, 'createPhoto.html', {'categories': Category.objects.all()})

def validatePhotoForm(request):
    if request.POST['title'] != null and request.POST['category'] != null:
        if len(request.POST['title']) >= 2:
            return True
        else:
            return 'Title Lenght > 2 \n Or Category Is Null'
    else:
        return 'Some Field Is Empty !'

def photosByUserId(request):
    categories = Category.objects.all()
    userPhotos = Photo.objects.filter(user= User.objects.get(id= request.session['user_id']))
    return render(request, 'myGallery.html', {'photos': userPhotos, 'categories': categories})

def photosByCategory(request, category):
    categories = Category.objects.all()
    photos = Photo.objects.filter(category= Category.objects.filter(name= category).values('id')[0]['id'])
    return render(request, 'photoByCategory.html', {
        'category': category,
        'categories': categories,
        'photos': photos
    })

def deleteFile(photo):
    path = str(photo.path)
    os.remove(path[1:])

def delete(request, delete):
    if(userOwner):
        photo = Photo.objects.get(id= delete)
        # delete refrences categorys in photo_category table
        removeCategory(photo)

        #delete file from media
        deleteFile(photo)
        
        #delete photo from table
        Photo.objects.filter(id= delete).delete()
        return photosByUserId(request)
    else:
        return HttpResponse('Error 403! Access Denied')

def editForm(request, edit):
    photo = Photo.objects.get(id= edit)
    categories = Category.objects.all()
    return render(request, 'editPhoto.html', {'photo': photo, 'categories': categories})

def edit(request, edit):
    if(userOwner):
        if validatePhotoForm(request) == True:
            photo = Photo.objects.get(id= edit)
            # delete refrences categorys in photo_category table
            removeCategory(photo)
            addCategory(request, photo)

            photo.title = request.POST['title']
            photo.description = request.POST['description']
            photo.save()
            return photosByUserId(request)
        else:
            return render(request, 'editPhoto.html', {'error': validatePhotoForm(request), 'categories': Category.objects.all()})
    else:
        return HttpResponse('Error 403! Access Denied')