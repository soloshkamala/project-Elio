from django import forms
from .models import MoodEntry

class MoodForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['date_time', 'mood_level', 'note', 'had_panic_attack']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'note': forms.Textarea(attrs={'placeholder': 'Що у тебе на думці?', 'rows': 4, 'class': 'form-input'}),
            'mood_level': forms.Select(attrs={'class': 'form-input'}),
        }