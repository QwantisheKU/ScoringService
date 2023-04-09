from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Calculation, CalculationResult, Profile
from .forms import CalculationForm, CalculationResultForm, SignUpForm, SignInForm, ContactForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import get_user_model
from .utils import paginate_calculations, check_recommendations, create_word_results
from django.http import FileResponse
from django_ratelimit.decorators import ratelimit
from docx2pdf import convert
User = get_user_model()
import pickle
import script
import time
import os
import glob

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
    calculations_results = CalculationResult.objects.all().filter(user=request.user).order_by('-date_created')

    results = 5
    custom_range, calculations_results = paginate_calculations(request, calculations_results, results)

    context = {'calculations_results': calculations_results, 'custom_range': custom_range}
    return render(request, 'scoring_app/home.html', context)

@login_required(login_url='sign-in')
def calculation(request):
    calculation_form = CalculationForm()
    calculation_result_form = CalculationResultForm()
    context = {'form': calculation_form}
    
    if request.method == 'POST':
        calculation_form = CalculationForm(request.POST)
        calculation_id = None
        data = [int(request.POST.get('person_age')), int(request.POST.get('person_income')), request.POST.get('person_home_ownership'), int(request.POST.get('person_emp_length')), request.POST.get('loan_intent'), int(request.POST.get('loan_amnt')), float(request.POST.get('loan_int_rate')), request.POST.get('cb_person_default_on_file'), int(request.POST.get('cb_person_cred_hist_length'))]
        if calculation_form.is_valid():
            saved_calculation_form = calculation_form.save(commit=False)
            saved_calculation_form.user = request.user
            saved_calculation_form = calculation_form.save()
            calculation_id = saved_calculation_form.pk
            request.session['data'] = data
        score = script.preprocess_data(data)[0]
        score_dict = {'score': score, 'calculation_id': calculation_id}
        calculation_result_form_query_dict = QueryDict('', mutable=True)
        calculation_result_form_query_dict.update(score_dict)
        calculation_result_form = CalculationResultForm(calculation_result_form_query_dict)
        print(calculation_result_form.is_valid())
        if calculation_result_form.is_valid():
            saved_calculation_result_form = calculation_result_form.save(commit=False)
            saved_calculation_result_form.user = request.user
            saved_calculation_result_form.save()
            return redirect(f'../result/{saved_calculation_form.pk}')
    return render(request, 'scoring_app/form.html', context)


@login_required(login_url='sign-in')
def contact(request):
    contact_form = ContactForm()
    context = {'contact_form': contact_form}
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            subject = 'Feedback'
            body = {
                'name': contact_form.cleaned_data['name'],
                'email': contact_form.cleaned_data['email'],
                'message': contact_form.cleaned_data['message'],
            }
            message = '\n'.join(body.values())

            try:
                send_mail(subject, message, 'finn4443@gmail.com', ['finn4443@gmail.com'])
            except BadHeaderError:
                return redirect('../home/')
    return render(request, 'scoring_app/contact.html', context)

@login_required(login_url='sign-in')
def get_calculation_result(request, calculation_id):
    recommendations = check_recommendations(request, calculation_id)
    try:
        calculation_result = CalculationResult.objects.get(calculation_id = calculation_id)
        calculation_result_form = CalculationResultForm(instance=calculation_result)
        request.session['score'] = calculation_result.score
        request.session['recommendations'] = recommendations
        context = {'calculation_result_form': calculation_result_form, 'recommendations': recommendations}
        return render(request, 'scoring_app/result.html', context)
    except Exception:
        return redirect('../home/')

@login_required(login_url='sign-in')
def download_result(request):
    # Works poorly with pdf convertion, problem with simultanious proccesses
    # TODO
    files = glob.glob('static/files/*.pdf')
    for f in files:
        os.remove(f)
    print_query = {}
    score = request.session.get('score')
    recommendations = request.session.get('recommendations')
    print_query['score'] = score
    print_query['recommendations'] = recommendations
    create_word_results(print_query)
    word_file = FileResponse(open('static/files/Результат расчета.docx', 'rb'))
    #convert('static/files/Результат расчета.docx', 'static/files/Результат расчета.pdf')
    #pdf_file = FileResponse(open('static/files/Результат расчета.pdf', 'rb'))
    final_format = None
    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'word':
            final_format = word_file
        #elif format == 'pdf':
            #final_format = pdf_file
    return final_format

@login_required(login_url='sign-in')
def delete_calculation(request, calculation_id):
    calculation = Calculation.objects.get(id = calculation_id)
    context = {}
    if request.method == "POST":
        calculation.delete()
        return redirect('../../home')
    return render(request, 'scoring_app/delete_calculation.html', context)

@login_required(login_url='sign-in')
def profile(request):
    user = request.user
    profile = Profile.objects.filter(user=user).exists()
    
    if not profile:
        profile_dict = {'email': request.user.email, 'user': request.user}
        profile_form_query_dict = QueryDict('', mutable=True)
        profile_form_query_dict.update(profile_dict)
        profile_form = ProfileForm(profile_form_query_dict)
        if profile_form.is_valid():
            saved_profile_form = profile_form.save(commit=False)
            saved_profile_form.user = request.user
            saved_profile_form.save()
        profile_form = saved_profile_form
    else:
        profile_form = Profile.objects.get(user=request.user)
    
    profile = request.user.profile
    profile_form = ProfileForm(instance=profile)
    context = {'profile_form': profile_form}

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('../profile/')
    
    return render(request, 'scoring_app/profile.html', context)

