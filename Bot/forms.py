from django import forms
from django.forms.widgets import RadioSelect


CHOICES=[('Extremely ','Extremely '),
         ('Very','Very'),
         ('Moderately','Moderately'),
         ('Slightly','Slightly'),
         ('Not at all','Not at all'),]

CHOICES2=[('Very Likely','Very Likely'),
         ('Likely','Likely'),
         ('Undecided','Undecided'),
         ('Unlikely','Unlikely'),
         ('Very Unlikely','Very Unlikely'),]

class SurveyForm(forms.Form):
    Question1 = forms.ChoiceField(label='Q1. How easy was the interaction?',choices=CHOICES, widget=forms.RadioSelect())
    Question2 = forms.ChoiceField(label='Q2. How engaging was it compared to a standard survey', choices=CHOICES, widget=forms.RadioSelect())
    Question3 = forms.ChoiceField(label='Q3. How enjoyable was it?',choices=CHOICES, widget=forms.RadioSelect())
    Question4 = forms.ChoiceField(label='Q4. How likely are you to use it again?', choices=CHOICES2, widget=forms.RadioSelect())
    Question5 = forms.ChoiceField(label='Q5. How likely are you to recommend it to someone else?', choices=CHOICES2, widget=forms.RadioSelect())
    Question6 = forms.ChoiceField(label='Q6. How intuitive did you find it? ', choices=CHOICES, widget=forms.RadioSelect())
    Question7 = forms.CharField(label='Q7. Did you learn anything?')
    Question8 = forms.CharField(label='Q8. Do you have any feedback?')

class IndexForm(forms.Form):
    post = forms.CharField()

class ConsentForm(forms.Form):
    post = forms.CharField()

class PISForm(forms.Form):
    post = forms.CharField()

class ResetForm(forms.Form):
    post = forms.CharField()