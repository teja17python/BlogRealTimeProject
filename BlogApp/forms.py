from  django import forms
from BlogApp.models import Comment,Post
from django.contrib.auth.models import User
class EmailSendForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')


class SignupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password']

class postform(forms.ModelForm):
    class Meta:
        model=Post
        fields = '__all__'
