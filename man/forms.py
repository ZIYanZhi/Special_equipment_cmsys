import re

from django import forms
from django.core.exceptions import ValidationError


# def phone_validate(value):
#    phone_re = re.compile(r'^1[3456789]\d{9}$')
#    if not phone_re.match(value):
#        raise ValidationError('手机格式错误')


class ManForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False,
                            widget=forms.TextInput({'class': 'form-control', 'disabled': 'disabled'}))
    name = forms.CharField(label='领取人', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # validators=[phone_validate, ],

