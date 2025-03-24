from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review, Place

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
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

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