from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import login

from .models import Listing, ListingImage, Category, Inquiry, Profile
from .forms import ListingForm, ListingImageForm, InquiryForm, SignUpForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def listing_list(request):
  listings = Listing.objects.filter(is_available=True)
  categories = Category.objects.all()

  #my search query
  query = request.GET.get('q')
  if query:
    listings = listings.filter(
      Q(title__icontains=query) | Q(description__icontains=query)
    )

  #category filters
  category_slug = request.GET.get('category')
  if category_slug:
    listings = listings.filter(category__slug=category_slug)
  
  paginator = Paginator(listings, 6)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  context = {
    'page_obj': page_obj,
    'categories': categories,
    'selected_category': category_slug,
    'query': query,
  }
  return render(request, 'consentform/listing_list.html', context)

def listing_detail(request, pk):
  listing = get_object_or_404(Listing, pk=pk)

  if request.method == 'POST':
    if not request.user.is_authenticated:
      messages.error(request, "You must be logged in to send an inquiry.")
      return redirect('login')
    
    inquiry_form = InquiryForm(request.POST)
    if inquiry_form.is_valid():
      inquiry = inquiry_form.save(commit=False)
      inquiry.listing = listing
      inquiry.sender = request.user
      inquiry.receiver = listing.owner
      inquiry.save()
      messages.success(request, "Your inquiry has been sent to the owner.")
  
  else:
    inquiry_form = InquiryForm()

  context = {
    'listing': listing,
    'inquiry_form': inquiry_form,
  }
  return render(request, 'consentform/listing_detail.html', context)

@login_required
def listing_create(request):
  ImageFormSet = inlineformset_factory(
    Listing, ListingImage, form=ListingImageForm, extra=3, can_delete=False
  )
  if request.method == 'POST':
    form = ListingForm(request.POST)
    formset = ImageFormSet(request.POST, request.FILES)

    if form.is_valid() and formset.is_valid():
      listing = form.save(commit=False)
      listing.owner = request.user
      listing.save()
      #attaching the uploaded image stuff to the listing

      formset.instance = listing
      formset.save()

      messages.success(request, "Listing created successfully!")
      return redirect('listing_detail', pk=listing.pk)
    
  else:
    form = ListingForm()
    formset = ImageFormSet()

  context = {
    'form': form,
    'formset': formset,
    'title': 'Create New Listing',
  }
  return render(request, 'consentform/listing_form.html', context)

@login_required
def listing_update(request, pk):
  listing = get_object_or_404(Listing, pk=pk)

  #security check feature to prevent unauthorized users from editing
  if listing.owner != request.user:
    messages.error(request, "You are not authorized to edit this listing.")
    return redirect('listing_detail', pk=listing.pk)
  
  ImageFormSet = inlineformset_factory(
    Listing, ListingImage, form=ListingImageForm, extra=1, can_delete=True
  )
  if request.method == 'POST':
    form = ListingForm(request.POST, instance=listing)
    formset = ImageFormSet(request.POST, request.FILES, instance=listing)

    if form.is_valid() and formset.is_valid():
      form.save()
      formset.save()
      messages.success(request, "Listing updated successfully!")
      return redirect('listing_detail', pk=listing.pk)
  else:
    form = ListingForm(instance=Listing)
    formset = ImageFormSet(instance=Listing)

  context = {
    'form': form,
    'formset': formset,
    'title': 'Edit Listing',
  }
  return render(request, 'consentform/listing_form.html', context)

@login_required
def listing_delete(request, pk):
  listing = get_object_or_404(Listing, pk=pk)

  if listing.owner != request.user:
    messages.error(request, "You are not authorized to delete this listing.")
    return redirect('listing_detail', pk=listing.pk)
  
  if request.method == 'POST':
    listing.delete()
    messages.success(request, "Listing deleted successfully.")
    return redirect('listing_list')
  
  context = {
    'listing': listing
  }
  return render(request, 'consentform/listing_delete.html', context)

@login_required
def dashboard(request):
  received_inquiries = Inquiry.objects.filter(
    reciever=request.user
  ).select_related('listing', 'sender')

  sent_inquiries = Inquiry.objects.filter(
    sender=request.user
  ).select_related('listing', 'receiver')

  #for counting unread but received messages
  unread_count = received_inquiries.filter(is_read=False).count()

  context = {
    'received_inquiries': received_inquiries,
    'sent_inquiries': sent_inquiries,
    'unread_count': unread_count,
  }
  return render(request, 'consentform/dashboard.html', context)

@login_required
def toggle_inquiry_read(request, pk):
  inquiry = get_object_or_404(Inquiry, pk=pk, receiver=request.user)

  inquiry.is_read = not inquiry.is_read
  inquiry.save()

  status_label = "read" if inquiry.is_read else "unread"
  messages.success(request, f"inquiry marked as {status_label}.")
  return redirect('dashboard')

#to delete an inquiry
@login_required
def delete_inquiry(request, pk):
  #feature to allow the detection if user is a sender or receiver
  inquiry = get_object_or_404(Inquiry, pk=pk)
  if request.user == inquiry.sender or request.user == inquiry.receiver:
    inquiry.delete()
    messages.success(request, "Inquiry deleted successfully.")
  else:
    messages.error(request, "You are not authorized to delete this inquiry.")
  return redirect('dashboard')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('listing_list')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in automatically after sign-up
            login(request, user)
            messages.success(request, f"Welcome to Campus Marketplace, {user.username}!")
            return redirect('listing_list')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile_edit(request):
  created = Profile.objects.get_or_create(user=request.user)

  if request.method == 'POST':
      u_form = UserUpdateForm(request.POST, instance=request.user)
      p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

      if u_form.is_valid() and p_form.is_valid():
          u_form.save()
          p_form.save()
          messages.success(request, "Your profile has been updated!")
          return redirect('dashboard')
  else:
      u_form = UserUpdateForm(instance=request.user)
      p_form = ProfileUpdateForm(instance=request.user.profile)

  context = {
      'u_form': u_form,
      'p_form': p_form,
  }
  return render(request, 'consentform/profile_edit.html', context)