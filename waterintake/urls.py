"""
URL configuration for waterintake project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from healthyfy import views
from django.views.generic.base import RedirectView

urlpatterns = [
     path('admin/', admin.site.urls),
    path('', views.healthyfy, name='home'),
    path('accounts/login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('logout/', views.logout_page, name='logout'),
     path('add_intake/', views.add_intake, name='add_intake'),
    path('intake_history/', views.intake_history, name='intake_history'),
     path('intake_list/', views.intake_list, name='intake_list'),
    path('find_difference/', views.find_difference, name='find_difference'),
    path('update/<int:id>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),

]
