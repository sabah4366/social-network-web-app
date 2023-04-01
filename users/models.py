from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from datetime import datetime
# Create your models here.
class PostModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ImageField(upload_to='photos/post',blank=False,null=False)
    description=models.TextField(max_length=1000,blank=True,null=True)
    location=models.CharField(max_length=200,blank=True,null=True,default="unknown")
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    created=models.DateTimeField(default=datetime.now)
    likes=models.ManyToManyField(User,related_name='likes')
    
    

    def __str__(self) -> str:
        return self.user.username


class CommentModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    post=models.ForeignKey(PostModel,on_delete=models.CASCADE)
    comment=models.CharField(max_length=1000,blank=True)
    created=models.DateTimeField(default=datetime.now)

    def __str__(self) -> str:
        return self.comment
class SaveModel(models.Model):
    post=models.ForeignKey(PostModel,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username