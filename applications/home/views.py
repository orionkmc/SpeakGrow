# Django
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    View,
)
from django.views.generic.edit import (
    FormView
)
from django.contrib.auth.mixins import LoginRequiredMixin

# Apps
from .forms import (LoginForm, UserRegisterForm)
from .models import (AnonymousUser, Room, UserProfile)


def get_client_ip(request):
    """  Getting client Ip"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class Home(LoginRequiredMixin, View):
    def get(self, req, *args, **kargs):
        ip_adresse = get_client_ip(req)
        obj, created = AnonymousUser.objects.get_or_create(
            ip_address=ip_adresse,
            defaults={},
        )
        try:
            Room.objects.create(
                speaker=UserProfile.objects.get(user__username=req.user),
                anonymousUser=obj
            )
        except Exception as e:
            raise e

        return render(req, 'home/home.html', {
            'form_login': LoginForm(),
            'register_login': UserRegisterForm(),
            "ip_adresse": ip_adresse
        })


class Login(FormView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:home')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(Login, self).form_valid(form)


class Register(View):
    def get(self, req, *args, **kargs):
        return render(req, 'user/register.html', {
            'form': UserRegisterForm(),
        })

    def post(self, req, *args, **kwargs):
        form = UserRegisterForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    'home_app:login'
                )
            )
        return render(req, 'user/register.html', {
            'form': form,
        })


class LogoutView(View):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'home_app:login'
            )
        )
