from django import forms
from .models import Account, UserProfile
from django.contrib.auth.models import User
'''class AccountForm(forms.ModelForm):
    class Meta:
        model='Account'
        fields=['first_name','last_name','phone_number','email','password']'''
class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('first_name','last_name','email')
    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        for fields in self.fields:
            self.fields[fields].widget.attrs['class']='form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False,error_messages={'invalid':("image files only")},widget=forms.FileInput)
    class Meta:
        model=UserProfile
        fields=('address_line_1','address_line_2','profile_picture','city','state','country')
    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for fields in self.fields:
            self.fields[fields].widget.attrs['class']='form-control'
