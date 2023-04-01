from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PostModel,CommentModel,SaveModel
from django.db.models import Q
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


def signinRequired(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'you must login')
            return redirect('signin')
        else:
            return fn(request,*args,**kwargs)
        
    return wrapper
desc=[never_cache,signinRequired]

@login_required(login_url='signin')
def home(request):
    posts=PostModel.objects.all().order_by('-created')
    saves=SaveModel.objects.filter(user=request.user)
    savelist=[]
    for sv in saves:
        savelist.append(sv.post.id)
    
    return render(request,'users/home.html',{"posts":posts,"savelist":savelist})

@login_required(login_url='signin')
def search_users(request):
    if request.method=="GET":
        users=request.GET.get('users')
        if users:
            users=Profile.objects.filter(
                Q(user__username__contains=users)|
                Q(user__first_name__contains=users)
            )
        return render(request,"users/search-page.html",{"users":users})
    return render(request,"users/search-page.html")


@login_required(login_url='signin')
def explore(request):
    if request.method =="GET":
        posts=PostModel.objects.all()
    return render(request,"users/explore-page.html",{"posts":posts})


@login_required(login_url='signin')
def notification(request):
    user=User.objects.get(user=request.user.id)
    profile=Profile.objects.get(user=request.user)
    followers=profile.follower.all()
    following=profile.user.follower.all()
   
    return render(request,"users/notification-page.html",{"followers":followers,"following":following})





@login_required(login_url='signin')
def profile(request):
    user=User.objects.get(id=request.user.id)
    posts=PostModel.objects.filter(user=user)
    profile=Profile.objects.get(user=request.user)
    post_count=len(posts)
    followers=len(profile.follower.all())
    following=len(profile.user.follower.all())

    if request.method=="GET":
        profile=Profile.objects.get(user=request.user)
    return render(request,"users/profile-page.html",{"profile":profile,"posts":posts,"post_count":post_count,"followers":followers,"following":following})

@login_required(login_url='signin')   
def other_user_profile(request,pk):
    user=User.objects.get(id=pk)
    profile=Profile.objects.get(user_id=pk)
    posts=PostModel.objects.filter(user=user)
    post_count=len(posts)
    if request.method=="GET":
        profile=Profile.objects.get(user_id=pk)
        if profile.follower.filter(id=request.user.id):
            msg=True
        else:
            msg=False
        user=User.objects.get(id=pk)
        posts=PostModel.objects.filter(user=user)
        followers=len(profile.follower.all())
        following=len(profile.user.follower.all())
        

        return render(request,'users/other-user-profile.html',{"user":user,"profile":profile,"posts":posts,"post_count":post_count,"msg":msg,"following":following,"followers":followers})

    

@login_required(login_url='signin')
def saved(request,pk):
    user=User.objects.get(id=request.user.id)
    post=PostModel.objects.get(user=pk)
    profile=Profile.objects.get(user_id=request.user.id)
    savepost=SaveModel(user=user,post=post,profile=profile)
    savepost.save()   
    return redirect('home')

@login_required(login_url='signin')
def unsave(request,pk):
    user=User.objects.get(id=request.user.id)
    post=PostModel.objects.get(id=pk)
    saves=SaveModel.objects.get(post=post,user=user)
    profile=Profile.objects.get(user_id=request.user.id)
    saves.delete()

    return redirect('home')
    # return render(request,"users/saved-post.html")

# @login_required(login_url='signin')
# def settings(request):
    
#     return render(request,"users/settings.html")



@login_required(login_url='signin')
def savedposts(request):
    user=User.objects.get(id=request.user.id)
    savedpost=SaveModel.objects.filter(user=user)


    return render(request,'users/saved-post.html',{'savedpost':savedpost})



@login_required(login_url='signin')
def update_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    if request.method=="GET":
        profile=Profile.objects.get(user_id=request.user.id)
        user=User.objects.get(id=request.user.id)
        return render(request,"users/update-profile.html",{"profilepic":profile.profile_pic,"user":user,"profile":profile})
    elif request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['username']
        email=request.POST['email']
        phone_no=request.POST['phone-no']
        bio=request.POST['bio']
        profile_pic=request.FILES.get('profile-picture')

        if User.objects.filter(username=username).exists() and (username!=request.user.username):
            messages.error(request,"username already exists try another username")
            return redirect('update-profile')
        elif User.objects.filter(email=email).exists() and (email != request.user.email):
            messages.error(request,"email already exists try another email")
            return redirect("update-profile")
        elif Profile.objects.filter(phone_no=phone_no).exists() and (phone_no == profile.phone_no):
            messages.error(request,"Phone number already taken")
        else:
            user.username=username
            user.first_name=fname
            user.last_name=lname
            user.email=email
            user.save()
            profile.phone_no=phone_no
            profile.bio=bio
            profile.profile_pic=profile_pic
            profile.save()
            messages.success(request,"Your account has been has been successfully updated. ")

            return redirect('profile')

@login_required(login_url='signin')
def post(request):
    user=User.objects.get(id=request.user.id)
    profile=Profile.objects.get(user_id=request.user.id)
    if request.method=="GET":
        
        return render(request,'users/create-post.html')
    if request.method=="POST":
        post=request.FILES.get('post')
        description=request.POST['description']
        location=request.POST['location']
        postuser=PostModel(post=post,description=description,location=location,profile=profile,user=user)
        postuser.save()

        return redirect('profile')
        
@login_required(login_url='signin')
def post_detail(request,pk):
    if request.method=="GET":
        post=PostModel.objects.get(id=pk)
        return render(request,"users/post-detail.html",{"post":post})


@method_decorator(desc,name='dispatch')
class PostUpdateView(UpdateView):
    template_name='users/post-update.html'
    model = PostModel
    fields = ['post','description','location']
    template_name_suffix = '_update_form'
    success_url=reverse_lazy('profile')

    def form_valid(self, form) :
        form.instance.user=self.request.user
        form.instance.profile.user=self.request.user
        messages.success(self.request,"Post has been updated ")
        return super().form_valid(form)


       
@login_required(login_url='signin')
def delete_post(request,pk):
    if request.method=="GET":
        PostModel.objects.get(id=pk).delete()
        messages.success(request,"post has been deleted")
        return redirect('profile')


     
@login_required(login_url='signin')
def comments(request,pk):
    post=post=PostModel.objects.get(id=pk)
    profile=Profile.objects.get(user=request.user)
    print(profile)
    if request.method=="GET":
        post=PostModel.objects.get(id=pk)
        comments=CommentModel.objects.filter(post=post).order_by('-created')
        return render(request,'users/comments.html',{"post":post,"comments":comments})

    if request.method=="POST":
        comment=request.POST['comment']
        cmnt=CommentModel(comment=comment,user=request.user,post=post,profile=profile)
        cmnt.save()
        return redirect('post-comment',post.id)


@login_required(login_url='signin')
def add_follow(request,pk):    
    if request.method=="POST":
        flwr=Profile.objects.get(user_id=pk)
        if flwr.follower.filter(id=request.user.id):
            flwr.follower.remove(request.user)
            flwr.save()
            return redirect('other-user',flwr.profile_id)
        else:
            flwr.follower.add(request.user)
            flwr.save()
            return redirect('other-user' ,flwr.profile_id)
   