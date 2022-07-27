from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from MembersApp.templates.regform import RegisterForm

# Create your views here.
def user_login(request):
    login_success = None
    if request.method == "POST":
        user_name = request.POST['user_name']
        user_pass = request.POST['user_pass']
        user = authenticate(request, username=user_name, password=user_pass)
        if user is not None:
            login(request, user)
            return redirect('/?login_success=True')
        else:
            return redirect('/members/login?login_success=False')
    
    if 'login_success' in request.GET:
        login_success = False
    return render(request, 'login.html', {'login_success':login_success})

def user_logout(request):
    logout(request)
    return redirect('/?logged_out=True')

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/?registered=True')
    else:
        form = RegisterForm()

    return render(request, 'register_user.html', {'form':form,})
		