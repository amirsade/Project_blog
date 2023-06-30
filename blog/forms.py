from django import forms
from .models import *


class TicketForm(forms.ModelForm):
    subject_choices = (
        ('Offers', 'Offers'),
        ('Critics', 'Critics'),
        ('reports', 'reports')
    )
    subject = forms.ChoiceField(choices=subject_choices)

    class Meta:
        model = Ticket
        fields = ['name', 'phone', 'email', 'message']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and phone.isalpha():
            raise forms.ValidationError('Invalid phone number. Phone number must contain only digits.')
        return phone

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError('Invalid Name. Name must be at least 3 characters long.')
        if name.isdigit():
            raise forms.ValidationError('Invalid Name. Name cannot be entirely numeric.')
        return name


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['name', 'email', 'text']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError('Invalid Name. Name must be at least 3 characters long.')
        if name.isdigit():
            raise forms.ValidationError('Invalid Name. Name cannot be entirely numeric.')
        return name
