import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'phone_number', 'birth_date', 'gender')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        for field_name in self.fields:
            self.fields[field_name].required = True


        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'


        self.fields['phone_number'].initial = '+380'
        self.fields['phone_number'].widget.attrs['placeholder'] = '+380XXXXXXXXX'


    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '')

        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')


        if not re.match(r'^\+380\d{9}$', phone):
            raise ValidationError("Номер має бути у форматі +380 і містити 9 цифр.")

        return phone