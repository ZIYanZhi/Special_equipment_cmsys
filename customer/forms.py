import re

from django import forms
from django.core.exceptions import ValidationError


# def phone_validate(value):
#    phone_re = re.compile(r'^1[3456789]\d{9}$')
#    if not phone_re.match(value):
#        raise ValidationError('手机格式错误')


class CustomerForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False,
                            widget=forms.TextInput({'class': 'form-control', 'disabled': 'disabled'}))
    name = forms.CharField(label='工序', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # validators=[phone_validate, ],
    phone = forms.CharField(label='车间',  max_length=11,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='车号', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    jx = forms.CharField(label='机型', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    create_time = forms.CharField(label='创建时间', required=False, max_length=32,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))
