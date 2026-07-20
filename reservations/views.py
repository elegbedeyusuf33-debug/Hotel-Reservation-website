from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Room, Booking
from datetime import datetime, date
import secrets
import requests
from django.conf import settings


@login_required # <-- This forces the redirect to the login page if not logged in
def MakeReservation(request):
    if request.method == "POST":
        hotel_name = request.POST.get('hotel')
        cin_raw = request.POST.get('checkin', '').strip()
        cout_raw = request.POST.get('checkout', '').strip()
        gst = request.POST.get('guests')

        # User email fallback if guest isn't logged in
        user_email = request.POST.get('email') if not request.user.is_authenticated else request.user.email
        if not user_email:
            user_email = "guest@example.com" # Emergency fallback

        # 1. Reject if dates are empty
        if not cin_raw or not cout_raw:
            return redirect('/noreservation/')

        # 2. Convert date strings to YYYY-MM-DD
        cin = None
        cout = None
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
            try:
                if not cin:
                    cin = datetime.strptime(cin_raw, fmt).strftime("%Y-%m-%d")
                if not cout:
                    cout = datetime.strptime(cout_raw, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue

        if not cin or not cout:
            return redirect('/noreservation/')

        # 3. Fetch room safely using 'category'
        try:
            clean_hotel_name = str(hotel_name).strip().lower()
            booked_room = Room.objects.filter(category=clean_hotel_name).first()
            if not booked_room:
                booked_room = Room.objects.first()
        except:
            booked_room = None

        if not booked_room:
            from django.http import HttpResponse
            return HttpResponse("Error: No rooms found in your database.")

        amount = booked_room.price_per_night

        # 4. Save booking safely linked to the logged-in user
        paystack_ref = f"bk-{secrets.token_hex(8)}"
        booking = Booking.objects.create(
            user=request.user, # <-- Changed from current_user to request.user
            room=booked_room,
            check_in=cin,
            check_out=cout,
            total_amount=amount,
            paystack_reference=paystack_ref,
            is_paid=False
        )

        request.session['rdata'] = user_email

        # 5. Connect to Paystack API to initialize payment
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        # Paystack expects amount in KOBO (Naira * 100)
        amount_in_kobo = int(amount * 100)

        payload = {
            "email": user_email,
            "amount": amount_in_kobo,
            "reference": paystack_ref,
            "callback_url": f"https://elegbede.pythonanywhere.com/verify-payment/{paystack_ref}/"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()

            if response_data.get('status'):
                authorization_url = response_data['data']['authorization_url']
                return redirect(authorization_url)
            else:
                return HttpResponse(f"Paystack Initialization Error: {response_data.get('message')}")
        except Exception as e:
            return HttpResponse(f"Payment Connection Failed: {str(e)}")

    rooms = Room.objects.all()
    return render(request, "makereservation.html", {"rooms": rooms})


def Successful(request):
    if 'rdata' in request.session:
        data = {"msg": "Your reservation is successful."}
        del request.session['rdata']
        return render(request, "successful.html", data)
    else:
        return redirect("/noreservation")


def Noreservation(request):
    if 'rdata' not in request.session:
        data = {"msg": "You have not make a reservation kindly make a reservation. "}
        return render(request, "noreservation.html", data)


def SubmitSuccess(request):
     return render(request, "success.html")


def VerifyPayment(request, ref):
    try:
        booking = Booking.objects.get(paystack_reference=ref)
    except Booking.DoesNotExist:
        return HttpResponse("Error: Reservation order reference not found.")

    url = f"https://api.paystack.co/transaction/verify/{ref}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response_data.get('status') and response_data['data']['status'] == 'success':
            booking.is_paid = True
            booking.save()
            return redirect('/successful/')
        else:
            return HttpResponse(f"Payment Verification Failed: {response_data.get('message')}")

    except Exception as e:
        return HttpResponse(f"Connection Error during verification: {str(e)}")