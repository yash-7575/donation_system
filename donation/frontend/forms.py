from django import forms
from api.models import Donation


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['title', 'description', 'category', 'quantity', 'image_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(choices=[
                ('clothing', 'Clothing'),
                ('food', 'Food'),
                ('electronics', 'Electronics'),
                ('furniture', 'Furniture'),
                ('education', 'Education'),
                ('medical', 'Medical'),
                ('other', 'Other'),
            ]),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
        }