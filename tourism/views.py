from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Place, Category, Province, Review
from .forms import SearchForm, ReviewForm, SignUpForm
from django.http import HttpResponseNotAllowed
from django.contrib.auth import logout

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
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.place = place
            review.user = request.user
            review.save()
            messages.success(request, 'รีวิวของคุณถูกบันทึกเรียบร้อยแล้ว!')
            return redirect('place_detail', pk=place.pk)
    else:
        form = ReviewForm()
    
    context = {
        'place': place,
        'reviews': reviews,
        'form': form,
        'avg_rating': avg_rating,
    }
    return render(request, 'tourism/place_detail.html', context)

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