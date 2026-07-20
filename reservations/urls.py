from django.contrib import admin
from django.urls import path,include
from .views import *
from reservations.views import MakeReservation, VerifyPayment

app_name="reservations"
urlpatterns = [

    path("makereservation/",MakeReservation, name="makereservation"),
    path("successful/",Successful, name="successful"),
    path("noreservation/",Noreservation, name="noreservation"),
    path("success/",SubmitSuccess, name="success"),
    path("customreservation",CustomReservation, name="customreserve"),
    path("carhire",CarHire, name="carhire"),
    path('verify-payment/<str:ref>/', VerifyPayment, name='verify_payment'),
]