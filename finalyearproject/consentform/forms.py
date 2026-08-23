from django import forms
from .models import Listing, ListingImage, Inquiry, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['avatar', 'bio', 'phone_number', 'location']

class ListingForm(forms.ModelForm):
  class Meta:
    model = Listing
    fields = ['title','category','listing_type','condition','price', 'description','is_available']

class ListingImageForm(forms.ModelForm):
  class Meta:
    model = ListingImage
    fields = ['image', 'caption',]

class InquiryForm(forms.ModelForm):
  class Meta:
    model = Inquiry
    fields = ['message', 'contact_email', 'contact_phone']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'phone_number', 'location']