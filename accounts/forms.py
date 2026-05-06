import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'phone_number', 'birth_date', 'gender', 'bio', 'diploma_file')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        optional_fields = ['bio', 'diploma_file']

        for field_name in self.fields:
            if field_name not in optional_fields:
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

    def clean_diploma_file(self):
        file = self.cleaned_data.get('diploma_file')
        if file:
            if file.size > 5 * 1024 * 1024:
                raise ValidationError("Файл занадто великий. Максимум 5 МБ.")

            ext = file.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png']:
                raise ValidationError("Дозволені лише формати PDF, JPG або PNG.")
        return file

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if bio and len(bio) > 1000:
            raise ValidationError("Біографія занадто довга (максимум 1000 символів).")
        return bio