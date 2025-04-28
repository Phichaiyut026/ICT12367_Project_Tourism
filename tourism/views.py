import random
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed
from django.contrib.auth import logout
from .models import Place, Category, Province, Review, TeamMember, PlaceImage, ReviewImage
from .forms import SearchForm, ReviewForm, SignUpForm,PlaceSearchForm, PlaceForm


def home(request):
    featured_places = Place.objects.filter(is_featured=True)[:6]
    categories = Category.objects.all()
    provinces = Province.objects.all()

    context = {
        'featured_places': featured_places,
        'categories': categories,
        'provinces': provinces,
    }
    return render(request, 'tourism/home.html', context)


def place_list(request):
    form = SearchForm(request.GET)
    places = Place.objects.all().order_by('-created_at')

    if form.is_valid():
        query = form.cleaned_data.get('query')
        province = form.cleaned_data.get('province')
        category = form.cleaned_data.get('category')

        if query:
            places = places.filter(Q(name__icontains=query) | Q(description__icontains=query))

        if province:
            places = places.filter(province__name__icontains=province)

        if category:
            places = places.filter(categories__name__icontains=category)

    paginator = Paginator(places, 9)  # แสดง 9 รายการต่อหน้า
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
    }
    return render(request, 'tourism/place_list.html', context)


def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    reviews = place.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    nearby_places = Place.objects.exclude(id=pk).order_by('?')[:5]
    for nearby_place in nearby_places:
        nearby_place.distance = round(random.uniform(1, 10), 1)

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST, request.FILES)
        print("Form data:", request.POST)
        if form.is_valid():
            print("Rating from form:", form.cleaned_data['rating'])
            review = form.save(commit=False)
            review.place = place
            review.user = request.user
            review.save()
            images = request.FILES.getlist('images')
            for image in images[:5]:
                ReviewImage.objects.create(review=review, image=image)

            messages.success(request, 'รีวิวของคุณถูกบันทึกเรียบร้อยแล้ว!')
            return redirect('place_detail', pk=place.pk)
        else:
            print("Form errors:", form.errors)
    else:
        form = ReviewForm()

    has_parking_attr = hasattr(place, 'has_parking')
    has_restaurant_attr = hasattr(place, 'has_restaurant')
    has_wifi_attr = hasattr(place, 'has_wifi')
    has_restroom_attr = hasattr(place, 'has_restroom')

    context = {
        'place': place,
        'reviews': reviews,
        'form': form,
        'avg_rating': avg_rating,
        'nearby_places': nearby_places,
        'has_parking_attr': has_parking_attr,
        'has_restaurant_attr': has_restaurant_attr,
        'has_wifi_attr': has_wifi_attr,
        'has_restroom_attr': has_restroom_attr,
    }
    return render(request, 'tourism/places/place_detail.html', context)


def add_review(request, pk):
    place = get_object_or_404(Place, pk=pk)
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.place = place
            review.user = request.user
            review.save()

            # จัดการรูปภาพ
            images = request.FILES.getlist('images')
            for image in images[:5]:
                ReviewImage.objects.create(review=review, image=image)

            messages.success(request, 'รีวิวของคุณถูกบันทึกเรียบร้อยแล้ว!')
            return redirect('place_detail', pk=place.pk)
    return redirect('place_detail', pk=place.pk)


def category_places(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    places = Place.objects.filter(categories=category)

    paginator = Paginator(places, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'tourism/category_places.html', context)


def province_places(request, province_id):
    province = get_object_or_404(Province, pk=province_id)
    places = Place.objects.filter(province=province)

    paginator = Paginator(places, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'province': province,
        'page_obj': page_obj,
    }
    return render(request, 'tourism/province_places.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'บัญชีของคุณถูกสร้างเรียบร้อยแล้ว คุณสามารถเข้าสู่ระบบได้ทันที')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'tourism/signup.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return HttpResponseNotAllowed(['POST'])


@login_required
def profile(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'reviews': reviews,
    }
    return render(request, 'tourism/profile.html', context)


def about(request):
    team_members = TeamMember.objects.all()
    context = {
        'team_members': team_members
    }
    return render(request, 'tourism/about.html', context)

@staff_member_required
def manage_data(request):
    # สร้างฟอร์มค้นหา
    form = PlaceSearchForm(request.GET)
    
    # ดึงข้อมูลสถานที่ทั้งหมด
    places = Place.objects.all().select_related('province').prefetch_related('categories', 'images')
    
    # ฟิลเตอร์ตามฟอร์ม
    if form.is_valid():
        query = form.cleaned_data.get('query')
        province = form.cleaned_data.get('province')
        category = form.cleaned_data.get('category')
        
        if query:
            places = places.filter(name__icontains=query)
        if province:
            places = places.filter(province=province)
        if category:
            places = places.filter(categories=category)
    
    # การแบ่งหน้า
    paginator = Paginator(places, 10)  # แสดง 10 รายการต่อหน้า
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tourism/places/manage_data.html', {
        'form': form,
        'page_obj': page_obj
    })
@staff_member_required
def place_add(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_data')
    else:
        form = PlaceForm()
    return render(request, 'tourism/places/place_add.html', {'form': form})

@staff_member_required
def place_edit(request, pk):
    place = get_object_or_404(Place, pk=pk)
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            return redirect('manage_data')
    else:
        form = PlaceForm(instance=place)
    return render(request, 'tourism/places//place_edit.html', {'form': form, 'place': place})

@staff_member_required
def place_delete(request, pk):
    place = get_object_or_404(Place, pk=pk)
    if request.method == 'POST':
        place.delete()
        return redirect('manage_data')
    return render(request, 'tourism/places/place_delete.html', {'place': place})