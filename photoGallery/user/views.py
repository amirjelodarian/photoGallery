from atexit import register
import email
import re
from turtle import home
from unicodedata import name
from django.db import router
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from requests import post
from sqlalchemy import null
from user.models import User
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password

# Create your views here.
def logIn(request):
    request.session['user_id'] = User.objects.filter(email= request.POST['email'], password= request.POST['password']).values('id')[0]['id']

def logOut(request):
    user = request.session.get('user_id', None)
    request.session.flush()
    request.session.modified = True
    request.session['user_id'] = user
    request.session.modified = True
    if request.session['user_id'] == None:
        return redirect('home')
    else:
        request.session['user_id'] = None
        return redirect('home')

def loggedIn(request):
    if 'user_id' in request.session:
        if request.session['user_id'] != None: 
            return True
        else:
            return False
    else:
        return False

def registerForm(request):
    if loggedIn(request):
        return redirect('home')
    return render(request, 'register.html')

def createUser(request):
    if loggedIn(request):
        return redirect('home')
    try:
        if request.method == 'POST':
            if validateRegisterForm(request) == True:
                User.objects.create(name=request.POST['name'], email=request.POST['email'], password=request.POST['password'])
                logIn(request)
                return redirect('home')
            else:
                return render(request, 'register.html', {'error': validateRegisterForm(request)})
    except:
        return redirect('home')

def validateRegisterForm(request):
    if request.POST['name'] != null and request.POST['email'] != null and request.POST['password'] != null and request.POST['confirmPassword'] != null:
        if len(request.POST['name']) >= 2 and len(request.POST['password']) >= 8 and request.POST['confirmPassword'] == request.POST['password'] and request.POST['email'] != null:
            try:
                validate_email(request.POST['email'])
            except:
                return 'Email Not Valid'    
            else:
                if(User.objects.filter(email= request.POST['email']).exists()):
                    return 'Email Exists \n'    
                else:
                    return True
            
        else:
            return 'Name Lenght > 2 \n Password Length > 8 \n Confirm Password Dosent match'    
    else:
        return 'Some Field Is Empty !'

def validateLoginForm(request):
    if request.POST['email'] != null and request.POST['password']:
        if len(request.POST['password']) >= 8 and request.POST['email'] != null:
            try:
                validate_email(request.POST['email'])
            except:
                return 'Email Not Valid'    
            else:
                if(User.objects.filter(email= request.POST['email'], password= request.POST['password']).exists()):
                    return True  
                else:
                    return 'Email And Password Doesnt Match ! \n'
            
        else:
            return 'Name Lenght > 2 \n Password Length > 8 \n Confirm Password Dosent match'    
    else:
        return 'Some Field Is Empty !'

def loginForm(request):
    if loggedIn(request):
        return redirect('home')
    return render(request, 'login.html')

def loginUser(request):
    if loggedIn(request):
        return redirect('home')
    try:
        if request.method == 'POST':
            if validateLoginForm(request) == True:
                logIn(request)
                if loggedIn(request):
                    return redirect('home')
                else:
                    return render(request, 'login.html', {'error': validateLoginForm(request)})    
            else:
                return render(request, 'login.html', {'error': validateLoginForm(request)})
    except:
        return redirect('home')