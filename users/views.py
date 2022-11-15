from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm


def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            next_page = request.POST.get("next", "/")
            if not username or not password:
                return HttpResponse("Username or Password can't be empty")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"Logged in as {user.username}")
                response = HttpResponse()
                response.headers['HX-Redirect'] = next_page
                return response
            else:
                return HttpResponse("Username or Password didn't match")
        return render(request, 'users/login.html')
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
 
def logout(request):
    auth_logout(request)
    messages.info(request, "Logged out")
    next_page = request.GET.get("next") or "/"
    return redirect(next_page)
    
    
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                messages.success(request, f"Signed up as {user.username}")
                response = HttpResponse()
                response.headers['HX-Redirect'] = "/"#reverse('users:my_profile')
                return redirect("/")
            return render(request, 'users/partials/signupform.html', {'form': form})
        else:
            form = UserCreationForm()
        return render(request, 'users/signup.html', {'form': form})
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
    