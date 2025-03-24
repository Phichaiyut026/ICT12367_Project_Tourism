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
]