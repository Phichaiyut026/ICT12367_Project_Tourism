from django.contrib import admin
from .models import Category, Province, Place, Review, TeamMember,PlaceImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 3

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'is_featured', 'created_at')
    list_filter = ('province', 'categories', 'is_featured')
    search_fields = ('name', 'description')
    filter_horizontal = ('categories',)
    list_editable = ('is_featured',)
    date_hierarchy = 'created_at'
    inlines = [PlaceImageInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('place', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'user__username', 'place__name')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('student_id', 'first_name', 'last_name')
    ordering = ('order', 'student_id')
@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'title', 'order', 'is_main', 'created_at')
    list_filter = ('place', 'is_main')
    search_fields = ('place__name', 'title')
    ordering = ('place', 'order')

