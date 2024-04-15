from django import forms

from common.models import Customer, User, Outorder, Clothes, Man, Outbound



class OutboundForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False,
                            widget=forms.TextInput({'class': 'form-control', 'disabled': 'disabled'}))
    code = forms.CharField(label='出库单号', required=False, max_length=32,
                           widget=forms.TextInput(attrs={'class': 'form-control','disabled': 'disabled'}))

    customer = forms.ModelChoiceField(label='车位', queryset=Customer.objects.all(),
                                      widget=forms.Select({'class': 'selectpicker','data-live-search':'true'}))
    user = forms.ModelChoiceField(label='经手人', required=False, queryset=User.objects.all(),
                                  widget=forms.Select({'class': 'form-control'}))

    name = forms.ModelChoiceField(label='领取人', required=False, queryset=Man.objects.all(),
                                  widget=forms.Select({'class': 'selectpicker','data-live-search':'true'}))
    clothes = forms.ModelChoiceField(label='器材信息', queryset=Clothes.objects.all(),
                                     widget=forms.Select({'class': 'selectpicker', 'data-live-search': 'true',}))
    amount = forms.IntegerField(label='数量', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    create_time = forms.CharField(label='创建时间', required=False, max_length=32,
                                  widget=forms.TextInput(attrs={'class': 'form-control', }))
    clothes_id = forms.ModelChoiceField(
        label='机件信息',
        queryset=Clothes.objects.all(),
        widget=forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
        required=False,
        to_field_name='id',
        empty_label='选择机件信息',
    )


class OutorderClothesForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False,
                            widget=forms.TextInput({'class': 'form-control', 'disabled': 'disabled'}))
    outorder = forms.ModelChoiceField(label='出库单号', required=False, queryset=Outorder.objects.all(),
                                      widget=forms.Select({'class': 'form-control'}))
    clothes = forms.ModelChoiceField(label='器材信息', queryset=Clothes.objects.all(),
                                     widget=forms.Select({'class': 'selectpicker','data-live-search':'true'}))
    amount = forms.IntegerField(label='数量', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    name = forms.ModelChoiceField(label='领取人', required=False, queryset=Man.objects.all(),
                                  widget=forms.Select({'class': 'selectpicker', 'data-live-search': 'true'}))

    create_time = forms.CharField(label='创建时间', required=False, max_length=32,
                                  widget=forms.TextInput(attrs={'class': 'form-control', }))


class EditmoreForm(forms.Form):
    clothes = forms.ModelChoiceField(label='器材', required=False, queryset=Clothes.objects.all(),
                                     widget=forms.Select({'class': 'form-control', 'disabled': 'disabled'}))
    amount = forms.IntegerField(label='数量', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    name = forms.ModelChoiceField(label='领取人', required=False, queryset=Man.objects.all(),
                                  widget=forms.Select({'class': 'selectpicker', 'data-live-search': 'true'}))

    create_time = forms.CharField(label='创建时间', required=False, max_length=32,
                                  widget=forms.TextInput(attrs={'class': 'form-control', }))
