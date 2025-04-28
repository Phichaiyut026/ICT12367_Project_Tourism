from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Place,Province, Category

class SearchForm(forms.Form):
    query = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'ค้นหาสถานที่ท่องเที่ยว...', 'class': 'form-control'})
    )
    province = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'จังหวัด', 'class': 'form-control'})
    )
    category = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'หมวดหมู่', 'class': 'form-control'})
    )

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, required=True) 
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), required=True)

    class Meta:
        model = Review
        fields = ['rating', 'comment']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
class PlaceSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ค้นหาสถานที่...'})
    )
    province = forms.ModelChoiceField(
        queryset=Province.objects.all(),
        required=False,
        empty_label='ทุกจังหวัด',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='ทุกหมวดหมู่',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = [
            'name', 'description', 'address', 'province', 'categories', 
            'image', 'is_featured', 'map_embed', 'has_parking', 
            'has_restaurant', 'has_wifi', 'has_restroom'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'province': forms.Select(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'map_embed': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'has_parking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_restaurant': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_wifi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_restroom': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }