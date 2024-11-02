from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUp
from django.contrib.auth import views as auth_views

def signup(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home:home')  # Redirect to the named URL 'profile'
    else:
        form = SignUp()
    return render(request, 'userlogin/signup.html', {'form': form})


    



