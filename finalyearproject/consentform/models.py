from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to="profiles/", default="profiles/default.png", blank=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)], null=True, blank=True )
    gender = models.CharField(max_length=10)
    location = models.CharField(max_length=100, blank=True, help_text="e.g. Hostels, Eastern Campus")

    def __str__(self):
      return f"{self.user.username}'s Profile"

class Category(models.Model):
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(max_length=50, unique=True)

  class Meta:
    verbose_name_plural = "categories"
  
  def __str__(self):
    return self.name

class Listing(models.Model):
  LISTING_TYPES = (
    ('item', 'Item for Sale/Rent'),
    ('service', 'Service offered'),
  )
  CONDITIONS = (
    ('new', 'Brand New'),
    ('like_new', 'Like New'),
    ('used', 'Fair / Used'),
    ('na', 'Not Applicable (Services)'),
  )
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='listings')

  title = models.CharField(max_length=150)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  listing_type = models.CharField(max_length=10, choices=LISTING_TYPES, default='item')
  condition = models.CharField(max_length=10, choices=CONDITIONS, default='used')

  is_available = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-created_at']
  
  def __str__(self):
    return self.title

class ListingImage(models.Model):
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
  image = models.ImageField(upload_to='listings/')
  caption = models.CharField(max_length=100, blank=True)

  def __str__(self):
    return f"Image for {self.listing.title}"

class Inquiry(models.Model):
  listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='inquiries')
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_inquiries')
  receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_inquiries')

  message = models.TextField()
  contact_email = models.EmailField()
  contact_phone = models.CharField(max_length=20, blank=True)

  created_at = models.DateTimeField(auto_now_add=True)
  is_read = models.BooleanField(default=False)

  class Meta:
    verbose_name_plural = 'Inquiries'
    ordering = ['-created_at']

  def __str__(self):
    return f"Inquiry on '{self.listing.title}' by {self.sender.username}"

class Review(models.Model):
  target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')

  rating = models.PositiveSmallIntegerField(
    validators = [MinValueValidator(1), MaxValueValidator(5)]
  )
  comment = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Review for {self.target_user.username} ({self.rating}/5)"