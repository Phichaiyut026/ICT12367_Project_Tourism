from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('places/', views.place_list, name='place_list'),
    path('places/<int:pk>/', views.place_detail, name='place_detail'),
    path('category/<int:category_id>/', views.category_places, name='category_places'),
    path('province/<int:province_id>/', views.province_places, name='province_places'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('places/<int:pk>/review/', views.add_review, name='add_review'),
    path('manage-data/', views.manage_data, name='manage_data'),
    path('manage-data/add/', views.place_add, name='place_add'),
    path('manage-data/edit/<int:pk>/', views.place_edit, name='place_edit'),
    path('manage-data/delete/<int:pk>/', views.place_delete, name='place_delete'),
]