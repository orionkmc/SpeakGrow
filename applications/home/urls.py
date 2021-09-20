# Django
from django.urls import path

# Apps
from applications.home.views import Home, Login, Register, LogoutView

app_name = "home_app"

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
]
