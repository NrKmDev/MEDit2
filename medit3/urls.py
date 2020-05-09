"""medit3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from contest.views import(
    home_screen_view,
    problems_view,
    standings_view,
)
from account.views import(
    registration_view,
    logout_view,
    login_view,
    profile_view,
    send_request,
    accept_request,
    other_profile_view,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_screen_view,name='home'),
    path('register/',registration_view,name='register'),
    path('logout/',logout_view,name='logout'),
    path('login/',login_view,name='login'),
    path('<int:contest_id>/problems/',problems_view,name='problems'),
    path('<int:contest_id>/standings/',standings_view,name='standings'),
    path('profile/',profile_view,name='profile'),
    path('send_request/<int:id>',send_request,name='send_request'),
    path('accept_request/<int:id>',accept_request,name='accept_request'),
    path('other_profile/<int:id>',other_profile_view,name='other_profile'),
]