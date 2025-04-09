from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import make_password
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

user = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=100,min_length=4)
    password1 = forms.CharField(max_length=10000,min_length=6,label="Password", widget=forms.PasswordInput(attrs={}))
    password2 = forms.CharField(max_length=10000,min_length=6,label="Confirmed Password", widget=forms.PasswordInput(attrs={}))
    
    class Meta:
        model = user
        fields = ['username','password1','password2','profile_picture']
        widgets = {
            'profile_picture':forms.FileInput(attrs={'class':'profile-pic-input'})
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if user.objects.filter(username=username).exists():
            raise forms.ValidationError('Invalid Username')
        return username

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1:
            raise forms.ValidationError('Password is invalid')
        if password1 != password2:
            raise forms.ValidationError("The passwords don't match")
        super(CustomUserCreationForm,self).clean()
        return self.cleaned_data

    def save(self,commit=True):
        user = super(CustomUserCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data.get('password2'))
        if commit:
            user.save()
        return user

class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=100,min_length=4)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'login-password-input',}))

    def clean(self):
        return super(AuthenticationForm,self).clean()