from django.contrib import admin
from .models import Profile, Category, Listing, ListingImage, Inquiry, Review

# Register your models here.
class ListingImageInline(admin.TabularInline):
  model = ListingImage
  extra = 3

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
  list_display = ('title', 'owner', 'category', 'price', 'listing_type', 'is_available', 'created_at')
  list_filter = ('listing_type', 'condition', 'is_available', 'category')
  search_fields = ('title', 'description', 'owner__username')
  inlines = [ListingImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'slug')
  prepopulated_fields = {'slug': ('name',)}

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'phone_number', 'location')

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
  list_display = ('listing', 'sender', 'receiver', 'is_read', 'created_at')
  list_filter = ('is_read', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
  list_display = ('target_user', 'author', 'rating', 'created_at')