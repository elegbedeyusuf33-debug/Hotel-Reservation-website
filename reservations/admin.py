from django.contrib import admin
from .models import UserEnquiryForm, Room, Booking

# 1. Register your user enquiry form so you can see customer messages
admin.site.register(UserEnquiryForm)

# 2. Register the Room model with columns so you can see prices and availability at a glance
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'category', 'price_per_night', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('room_number',)

# 3. Register the Booking model to track Paystack payments and guest dates
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in', 'check_out', 'is_paid', 'paystack_reference')
    list_filter = ('is_paid', 'check_in')
    search_fields = ('paystack_reference', 'user__username', 'room__room_number')