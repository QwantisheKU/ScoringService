from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
from .models import Calculation, CalculationResult
from .forms import CalculationForm, CalculationResultForm
import pickle
import script

def sign_up(request):
    return render(request, 'scoring_app/sign_up.html')

def sign_in(request):
    return render(request, 'scoring_app/sign_in.html')

def home(request):
    calculations = Calculation.objects.all()
    context = {'calculations': calculations}
    return render(request, 'scoring_app/home.html', context)

def form(request):
    calculation_form = CalculationForm()
    calculation_result_form = CalculationResultForm()
    context = {'form': calculation_form}
    score = []
    if request.method == 'POST':
        calculation_form = CalculationForm(request.POST)
        data = [int(request.POST.get('person_age')), int(request.POST.get('person_income')), request.POST.get('person_home_ownership'), int(request.POST.get('person_emp_length')), request.POST.get('loan_intent'), int(request.POST.get('loan_amnt')), float(request.POST.get('loan_int_rate')), request.POST.get('cb_person_default_on_file'), int(request.POST.get('cb_person_cred_hist_length'))]
        if calculation_form.is_valid():
            saved_calculation_form = calculation_form.save()
            request.session['calculation_id'] = saved_calculation_form.pk
            request.session['data'] = data
            score = script.preprocess_data(data)[0]
            score_dict = {'score': score, 'calculation_id': saved_calculation_form.pk}
            calculation_result_form_query_dict = QueryDict('', mutable=True)
            calculation_result_form_query_dict.update(score_dict)
            calculation_result_form = CalculationResultForm(calculation_result_form_query_dict)
            if calculation_result_form.is_valid():
                calculation_result_form.save()
            return redirect('../result/')
    return render(request, 'scoring_app/form.html', context)

def calculation_result(request):
    calculation_id = request.session.get('calculation_id')
    data = request.session.get('data')
    calculation_result_form = CalculationResultForm()
    score = script.preprocess_data(data)[0]
    context = {'score': score}
    score_dict = {'score': score, 'calculation_id': calculation_id}
    calculation_result_form_query_dict = QueryDict('', mutable=True)
    calculation_result_form_query_dict.update(score_dict)
    calculation_result_form = CalculationResultForm(calculation_result_form_query_dict)
    if calculation_result_form.is_valid():
        calculation_result_form.save()
    return render(request, 'scoring_app/result.html', context)

def contact(request):
    return render(request, 'scoring_app/contact.html')