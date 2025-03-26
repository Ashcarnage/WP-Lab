from django import forms

MANUFACTURER_CHOICES = [
    ('ford', 'Ford'),
    ('toyota', 'Toyota'),
    ('bmw', 'BMW'),
    ('honda', 'Honda'),
]

class CarForm(forms.Form):
    manufacturer = forms.ChoiceField(
        choices=MANUFACTURER_CHOICES,
        label="Manufacturer"
    )
    model_name = forms.CharField(
        max_length=50,
        label="Model Name"
    )