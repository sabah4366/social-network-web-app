from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.decorators import login_required






# Create your views here.


def signup(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        phone_no=request.POST['phone-no']
        bio=request.POST['bio']
        profile_pic=request.FILES.get('profile-picture')
        confirmpassword=request.POST['confirmpassword']
        if User.objects.filter(username=username).exists():
            messages.error(request,"username already exists try another username")
            return redirect('signup')
        elif not username.isalnum():
            messages.error(request,"username must be alpha-numeric")
            return redirect("signup")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"email already exists try another email")
            return redirect("signup")
        elif len(password)<8:
            messages.error("password must contain more than 8 characters")
            return redirect("signup")
        elif password!=confirmpassword:
            messages.error(request,"password does not match")
        elif Profile.objects.filter(phone_no=phone_no).exists():
            messages.error(request,"Phone number already taken")
        else:
            myuser=User(first_name=fname,last_name=lname,username=username,email=email,password=password)
            myuser.set_password(password)
            myuser.save()
            profile=Profile(profile_pic=profile_pic,bio=bio,phone_no=phone_no,user=myuser,profile_id=myuser.id)
            profile.save()
            messages.success(request,"Your account has been has been successfully created. ")

            return redirect('signin')

    return render(request,'accounts/signup.html')

def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser == True:
                messages.success(request,"You are successfully logined")
                return redirect('admin/')
            else:
                messages.success(request,"You are successfully logined")
                return redirect('home')
        else:
            messages.error(request,"invalid credentials")
            return redirect('signin')

    return render(request,'accounts/signin.html')


@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request,"You are logouted")
    return redirect('signin')

