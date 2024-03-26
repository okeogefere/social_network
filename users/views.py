from django.shortcuts import render, redirect
from users.forms import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from django.contrib.auth.decorators import login_required
# Create your views here.

user = settings.AUTH_USER_MODEL

# Create your views here.
def sign_in(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are logged in Already')
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in")
                return redirect('home')
            else:
                messages.warning(request, 'User does not Exist, Create an account')
        except:
            messages.warning(request, f"User with {email} does not exist")
    return render(request, 'users/sign-in.html')


def sign_up(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f" Hey {username} Your Account was Created Successfully")
            new_user = authenticate(username=form.cleaned_data['email'], 
                                    password=form.cleaned_data['password1'] 
                                    )
            login(request, new_user )
            return redirect('home')
    else:

        form = UserRegisterForm()
    return render(request, 'users/sign-up.html', {'form':form})


def sign_out(request):
    logout(request)
    messages.success(request, f" You are logged out")

    return redirect('sign-in')


@login_required
def profile(request):   
    user_profile = request.user.userprofile
    print(user_profile.user.email)
    return render(request, 'users/profile.html', {'user_profile': user_profile})


@login_required
def edit_profile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'users/edit-profile.html', {'form': form})


def settings(request):
    return render(request, 'users/settings.html')

def about(request):
    return render(request, 'users/about.html')

def photos(request):
    return render(request, 'users/photos.html')

