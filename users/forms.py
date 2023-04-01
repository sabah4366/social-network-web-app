from .models import PostModel,CommentModel
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model=PostModel
        fields="__all__"

        widgets={
            'post':forms.FileInput(attrs={'class':"form-control post invisible"}),
            'description':forms.Textarea(attrs={"class":"form-control "}),
            'location':forms.CharField(attrs={"class":"form-control location"})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=CommentModel
        fields="__all__"