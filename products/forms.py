from django import forms

from common.models import Customer, User, Outorder, Clothes, Man, Outbound

from django.forms import modelformset_factory

class VariantForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = ['id', 'code', 'customer', 'user', 'name', 'clothes', 'amount']
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'customer': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'clothes': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),

        }
VariantFormSet = modelformset_factory(Outbound, form=VariantForm)
