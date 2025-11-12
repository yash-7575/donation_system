# core/forms.py
from django import forms

class SignupStep1Form(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('donor','Donor'),('ngo','NGO'),('recipient','Recipient')])

class DonorProfileForm(forms.Form):
    name = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    pincode = forms.CharField(max_length=12, required=False)

class NGOProfileForm(forms.Form):
    ngo_name = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=20)
    website = forms.URLField(required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=12)

class RecipientProfileForm(forms.Form):
    name = forms.CharField(max_length=150)
    phone = forms.CharField(max_length=20, required=False)
    family_size = forms.IntegerField(min_value=1, initial=1)
    urgency = forms.ChoiceField(choices=[('low','Low'),('medium','Medium'),('high','High')], initial='medium')
    address = forms.CharField(widget=forms.Textarea, required=False)
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    pincode = forms.CharField(max_length=12, required=False)
