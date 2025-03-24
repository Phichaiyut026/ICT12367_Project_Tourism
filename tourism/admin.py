from django.contrib import admin
from .models import Category, Province, Place, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'is_featured', 'created_at')
    list_filter = ('province', 'categories', 'is_featured')
    search_fields = ('name', 'description')
    filter_horizontal = ('categories',)
    list_editable = ('is_featured',)
    date_hierarchy = 'created_at'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('place', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'user__username', 'place__name')