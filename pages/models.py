from django.db import models
from django.contrib.auth.models import User

# Changed the class name to UserEnquiryForm to match your form/views
class UserEnquiryForm(models.Model):
    names = models.CharField("Enter your names", max_length=255)
    email = models.CharField("Enter your email", max_length=255)
    phone = models.CharField("Enter your phone", max_length=255)
    enquiry = models.CharField("Enter your request", max_length=255)

    def __str__(self):
        return self.email

# An alias just in case your admin.py calls it UserEnquiryModel
UserEnquiryModel = UserEnquiryForm


class Room(models.Model):
    ROOM_CATEGORIES = (
        ('STANDARD', 'Standard Room'),
        ('DELUXE', 'Deluxe Room'),
        ('SUITE', 'Executive Suite'),
    )
    room_number = models.CharField("Room Number", max_length=10, unique=True)
    category = models.CharField(max_length=20, choices=ROOM_CATEGORIES, default='STANDARD')
    price_per_night = models.DecimalField("Price per Night (₦)", max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_category_display()} - Room {self.room_number}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservations")
    check_in = models.DateField()
    check_out = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paystack_reference = models.CharField(max_length=100, unique=True, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} for Room {self.room.room_number}"