"""
URL configuration for hotel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
app_name="pages"
urlpatterns = [
  path("",HomePage,name="homepage"),
  path("about",About,name="about"),
  path("contact",Contact,name="Contact"),
  path("services",Services,name="services"),
  path("requestsuccess",RequestSuccess,name="reqsuccess"),
  path("register", RegisterUser,name="registration"),
  path("sendemail",SendEmail,name="sendemail02"),
  path("dashboard", Dashboard,name="registration"),
  path("thankyou", Thanks,name="thankyou"),
  path("submit_form", submit_form,name="submit_form"),
  path("submit_reg", submit_form,name="submit_reg"),
  path("Kitchen", Kitchen,name="Kitchen"),
  path("laundry", Laundry,name="laundry"),
  path("initiatepay", initiatepay,name="initiatepay"),
  path("order/", Order,name="order"),
 ]
