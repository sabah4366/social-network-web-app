from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user')
    follower=models.ManyToManyField(User,related_name='follower')
    profile_id=models.BigAutoField(primary_key=True)
    bio=models.CharField(
        max_length=250,
        blank=True,
        null=True,

    )

    phone_no=models.IntegerField(
        blank=True,
        unique=True,
        null=True

    )
    profile_pic=models.ImageField(

        upload_to='photos/profile',
    )

    def __str__(self) -> str:
        return self.user.username