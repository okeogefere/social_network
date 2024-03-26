from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': "input100"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': "input100"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Email', 'class': "input100"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': "input100"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': "input100"})) 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)  
    email = forms.EmailField()  
    last_name = forms.CharField(max_length=150)
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'gender', 'status', 'occupation', 'lives_in', 'born_in', 'phone', 'dob', 'website', 'photos']

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'}),
            'bio': forms.Textarea(attrs={'rows':2}),
            'country': forms.Select(),
            'state': forms.Select(),
            'city': forms.Select(),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        user_instance = self.instance.user
        self.fields['first_name'].initial = user_instance.first_name 
        self.fields['email'].initial = user_instance.email  
        self.fields['last_name'].initial = user_instance.last_name  

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        user_instance = profile.user
        user_instance.first_name = self.cleaned_data['first_name']
        user_instance.email = self.cleaned_data['email']
        user_instance.last_name = self.cleaned_data['last_name']
        if commit:
            profile.save()
            user_instance.save()
        return profile