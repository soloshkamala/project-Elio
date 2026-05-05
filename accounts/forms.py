from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ElioRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        label="Твій нікнейм",
        help_text=None
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = None