from django.forms import ModelForm
from .models import Calculation, CalculationResult
from crispy_forms.helper import FormHelper

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
    'cb_person_cred_hist_length']
        
    def __init__(self, *args, **kwargs):
        super(CalculationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 

class CalculationResultForm(ModelForm):
    class Meta:
        model = CalculationResult
        fields = ['score', 'calculation_id']