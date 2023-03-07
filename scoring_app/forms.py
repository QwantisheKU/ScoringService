from django.forms import ModelForm
from .models import Calculation, CalculationResult
from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class SignInForm(AuthenticationForm):
    email = forms.EmailField(
        max_length=100,
        required = True,
        help_text='Введите email адрес',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    password = forms.CharField(
        help_text='Введите пароль',
        required = True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}),
    )
    class Meta:
        model = User
        fields = ['email', 'password']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        required = True,
        help_text='Введите email адрес',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    password1 = forms.CharField(
        help_text='Введите пароль',
        required = True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}),
    )
    password2 = forms.CharField(
        required = True,
        help_text='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}),
    )
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class CalculationForm(ModelForm):
    class Meta:
        model = Calculation
        fields = ['person_name',
    'person_age',
    'person_income',
    'person_home_ownership',
    'person_emp_length',
    'loan_intent',
    'loan_amnt',
    'loan_int_rate',
    'cb_person_default_on_file',
    'cb_person_cred_hist_length',
    ]
        
    def __init__(self, *args, **kwargs):
        super(CalculationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 

class CalculationResultForm(ModelForm):
    class Meta:
        model = CalculationResult
        fields = ['score', 'calculation_id']

