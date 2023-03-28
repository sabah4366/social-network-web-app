from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Profile


@login_required(login_url='signin')
def home(request):
    return render(request,'users/home.html')


def search(request):
    return render(request,"users/search-page.html")



def explore(request):
    return render(request,"users/explore-page.html")



def notification(request):
    return render(request,"users/notification-page.html")




def createpost(request):
    return render(request,"users/create-post.html")


def profile(request):
    if request.method=="GET":
        profile=Profile.objects.get(user=request.user)
    return render(request,"users/profile-page.html",{"profile":profile})


def saved(request):
    
    return render(request,"users/saved-post.html")

def settings(request):
    
    return render(request,"users/settings.html")