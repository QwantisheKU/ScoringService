from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Calculation, CalculationResult
from .forms import CalculationForm, CalculationResultForm, SignUpForm, SignInForm
from django.contrib.auth.decorators import login_required
import pickle
import script
import time

def sign_up(request):
    sign_up_form = SignUpForm()
    context = {'sign_up_form': sign_up_form}
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
            return redirect('../sign-in/')
    return render(request, 'scoring_app/sign_up.html', context)

def sign_in(request):
    #sign_in_form = SignInForm()
    #context = {'sign_in_form': sign_in_form}
    context = {}
    if request.method == 'POST':
        #sign_in_form = SignInForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('../home/')
    return render(request, 'scoring_app/sign_in.html', context)

@login_required(login_url='sign-in')
def sign_out(request):
    logout(request)
    return redirect('../sign-in/')

@login_required(login_url='sign-in')
def home(request):
    calculations = Calculation.objects.all().filter(user=request.user)
    context = {'calculations': calculations}
    return render(request, 'scoring_app/home.html', context)

@login_required(login_url='sign-in')
def form(request):
    calculation_form = CalculationForm()
    context = {'form': calculation_form}
    if request.method == 'POST':
        calculation_form = CalculationForm(request.POST)
        data = [int(request.POST.get('person_age')), int(request.POST.get('person_income')), request.POST.get('person_home_ownership'), int(request.POST.get('person_emp_length')), request.POST.get('loan_intent'), int(request.POST.get('loan_amnt')), float(request.POST.get('loan_int_rate')), request.POST.get('cb_person_default_on_file'), int(request.POST.get('cb_person_cred_hist_length'))]
        if calculation_form.is_valid():
            saved_calculation_form = calculation_form.save(commit=False)
            saved_calculation_form.user = request.user
            saved_calculation_form = calculation_form.save()
            request.session['data'] = data
            return redirect(f'../result/?calculation_id={saved_calculation_form.pk}')
    return render(request, 'scoring_app/form.html', context)

@login_required(login_url='sign-in')
def calculation_result(request):
    calculation_id = request.GET.get('calculation_id')
    data = request.session.get('data')
    calculation_result_form = CalculationResultForm()
    score = script.preprocess_data(data)[0]
    context = {'score': score}
    score_dict = {'score': score, 'calculation_id': calculation_id}
    calculation_result_form_query_dict = QueryDict('', mutable=True)
    calculation_result_form_query_dict.update(score_dict)
    calculation_result_form = CalculationResultForm(calculation_result_form_query_dict)
    if calculation_result_form.is_valid():
        saved_calculation_result_form = calculation_result_form.save(commit=False)
        saved_calculation_result_form.user = request.user
        saved_calculation_result_form.save()
    return render(request, 'scoring_app/result.html', context)

@login_required(login_url='sign-in')
def contact(request):
    return render(request, 'scoring_app/contact.html')