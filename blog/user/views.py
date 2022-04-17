from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from user.forms import (SignupForm, LoginForm)


def login_view(request):
    ''' Login View : Handles the login of user and on successfull login redirect them to home page'''
    context = {'title': 'Signup'}

    user = request.user

    if user.is_authenticated:
        # redirecting user to home page if already authenticated
        return redirect('home')

    # POST request
    elif request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(email=email, password=password)
            login(request, user)

            return redirect('home')
        else:
            context['form'] = form

    #GET request
    else:
        form = LoginForm()
        context['form'] = form

    return render(request, 'user/login.html', context)

def logout_view(request):
    '''Logout View : Handles the logging out of the user'''

    logout(request)
    return redirect('login')
