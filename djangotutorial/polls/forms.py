from django import forms
from django.forms import DateInput, TimeInput
from .models import Meeting

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            'date',
            'time',
            'duration',
            'description',
            'club',
            'room',
            'invited_count',
            'accepted_count'
        ]
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'time': TimeInput(attrs={'type': 'time'}),
        }
