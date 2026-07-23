from django.contrib import admin

from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city', 'property_type', 'listing_type', 'is_featured', 'is_available')
    list_filter = ('property_type', 'listing_type', 'is_featured', 'is_available', 'city')
    search_fields = ('title', 'description', 'city', 'address')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PropertyImageInline]
