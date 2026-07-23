from django.urls import path

from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('listings/', views.ListingListView.as_view(), name='property_list'),
    path('listings/<int:pk>/', views.ListingDetailView.as_view(), name='property_detail'),
]
