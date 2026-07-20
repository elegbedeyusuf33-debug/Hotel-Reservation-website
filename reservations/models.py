from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
    hotel = models.CharField('Select Hotel', max_length=100)
    names = models.CharField('Names', max_length=100)
    email = models.CharField('Email', max_length=100)
    phone = models.CharField('Phone ', max_length=100)
    chk_in = models.CharField('Check in', max_length=100)
    chk_out = models.CharField('Check out', max_length=100)
    guest = models.CharField('Number of guests', max_length=100)
    status = models.CharField('Status', max_length=100, default='pending')

    def __str__(self):
        return f"{self.email} - {self.names}"


class UserEnquiryForm(models.Model):
    names = models.CharField("Enter your names", max_length=255)
    email = models.CharField("Enter your email", max_length=255)
    phone = models.CharField("Enter your phone", max_length=255)
    enquiry = models.CharField("Enter your request", max_length=255)

    def __str__(self):
        return self.email


class Room(models.Model):
    # Updated categories to match your actual hotel and destination options
    HOTEL_CATEGORIES = (
        ('new_york', 'New York Luxury Suite'),
        ('paris', 'Paris Boutique Room'),
        ('shangrila', 'Shangri-La'),
        ('chatrium', 'Chatrium'),
        ('fourseasons', 'Four Seasons'),
        ('hilton', 'Hilton'),
    )
    room_number = models.CharField("Room/ID Number", max_length=10, unique=True)
    category = models.CharField(max_length=20, choices=HOTEL_CATEGORIES, default='hilton')
    price_per_night = models.DecimalField("Price per Night ($)", max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_category_display()} - Room {self.room_number}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservation_bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    check_in = models.DateField()
    check_out = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paystack_reference = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} for Room {self.room.room_number}"
