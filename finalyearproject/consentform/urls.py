from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

#CRUD ops......
urlpatterns = [
  path('', views.listing_list, name='listing_list'),
  path('create/', views.listing_create, name='listing_create'),
  path('<int:pk>/', views.listing_detail, name='listing_detail'),
  path('<int:pk>/edit', views.listing_update, name='listing_update'),
  path('<int:pk>/delete', views.listing_delete, name='listing_delete'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('inquiries/<int:pk>/toggle-read/', views.toggle_inquiry_read, name='toggle_inquiry_read'),
  path('inquiries/<int:pk>/delete/', views.delete_inquiry, name='delete_inquiry'),

    # Existing routes (Listings, Dashboard)...
  path('', views.listing_list, name='listing_list'),
  path('dashboard/', views.dashboard, name='dashboard'),

  # Authentication Routes
  path('signup/', views.signup_view, name='signup'),
  path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(next_page='listing_list'), name='logout'),
  
  # Profile Route
  path('profile/edit/', views.profile_edit, name='profile_edit'),
]
