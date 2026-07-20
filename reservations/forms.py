from django.forms import ModelForm 
from .models import  Reservation

class Rform(ModelForm):
      class Meta:
           model=Reservation
           fields=["hotel","names","email","phone","chk_in","chk_out"] 




