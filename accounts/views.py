from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages


# Create your views here.

class RegisterView(View):
    SECRET_CODE = "9321"

    def get(self, request):
        return render(request, "accounts/create_user.html")

    def post(self, request):
        username = request.POST['username'].strip()
        password = request.POST['password']
        password2 = request.POST['password2']
        secret_code = request.POST['secret_code']

        if not username:
            return render(request, "accounts/create_user.html", {'error': 'Brak użytkownika'})

        if secret_code != self.SECRET_CODE:
            return render(request, "accounts/create_user.html", {'error': 'Błędny kod'})

        if password != '' and password == password2:
            u = User(username=username, password=password)
            u.set_password(password)
            u.save()
            messages.success(request, 'Użytkownik został pomyślnie dodany.')
            return redirect('success_page')
        return render(request, "accounts/create_user.html", {'error': "Passwords don't match"})


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login_user.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            messages.success(request, 'Pomyślnie zalogowano')
            redirect_url = request.GET.get('next', 'success_page')
            login(request, user)
            return redirect(redirect_url)
        else:

            return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Wylogowano")
        return redirect('success_page')
