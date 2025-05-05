from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import make_password
from .forms import AuthenticationForm,CustomUserCreationForm

def login_view(request):
    context = {}
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username= username, password= password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    context['form'] = form
    return render(request, 'registration/login.html',context)

def logout_view(request):
    logout(request)
    return redirect('/')

def signup_view(request):
    context = {}
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            print('Thank you Jesus')
            return redirect('/')

    context['form'] = form
    return render(request, 'registration/signup.html', context)

def update_profile_view(request):
    if not request.user.is_authenticated:
        redirect('/')
    
    context = {}
    user = request.user

    form = CustomUserCreationForm(instance=user)
    context['form'] = form
    return render(request, "registration/profile_update.html", context)