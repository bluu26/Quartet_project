from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View


# Create your views here.

class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/create_user.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != '' and password == password2:
            u = User(username=username, password=password)
            u.save()
            return redirect('home')
        return render(request, "accounts/create_user.html", {'error': "Passwords don't match"})


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login_user.html')