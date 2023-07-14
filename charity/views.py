from django.shortcuts import render, redirect
from django.views import View
from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from .models import Institution, Donation, Category
from .forms import RegisterUserForm, LoginForm

class LandingPage(View):
    def get(self, request):
        institutions = Institution.objects.all()
        donations = Donation.objects.all()
        institutions_amount = len(institutions)
        bags_amount = 0
        for donation in donations:
            bags_amount += donation.quantity
        foundations = Institution.objects.filter(type=0)
        organizations = Institution.objects.filter(type=1)
        collections = Institution.objects.filter(type=2)

        return render(request, "index.html", context={"bags_amount": bags_amount, "institutions_amount": institutions_amount,
                                                      "foundations": foundations, "organizations": organizations,
                                                      "collections": collections})



class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()

        return render(request, 'form.html', context={"categories": categories, "institutions": institutions})


class Login(View):
    def get(self, request):
        form = LoginForm()
        return TemplateResponse(request, 'login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                #form.add_error(None, 'Login lub hasło się nie spina')
                return redirect('register')
        return TemplateResponse(request, 'login.html', context={'form': form})


class Register(View):
    def get(self, request):
        form = RegisterUserForm()
        return TemplateResponse(request, 'register.html', context={'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                #form.add_error('name', "email zajety")
                return redirect('register')
            elif form.cleaned_data['password'] != form.cleaned_data['password2']:
                #form.add_error(None, 'Hasła muszą być takie same')
                return redirect('register')
            else:
                User.objects.create_user(
                    username=email,
                    first_name=name,
                    last_name=surname,
                    password=password,
                    email=email
                )
                return redirect('login')
        return TemplateResponse(request, 'register.html', context={'form': form})


class Profile(View):

    def get(self, request):
        user = User.objects.get(id=self.request.user.id)
        return render(request, 'profile.html', context={'user': user})


