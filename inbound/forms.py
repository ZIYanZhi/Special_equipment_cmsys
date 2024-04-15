from django import forms

from common.models import Customer, User, Clothes, Inorder,Department


class InboundForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False,
                            widget=forms.TextInput({'class': 'form-control', 'disabled': 'disabled'}))
    code = forms.CharField(label='入库单号', required=False, max_length=32,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    clothes = forms.ModelChoiceField(label='器材信息', queryset=Clothes.objects.all(),
                                     widget=forms.Select({'class': 'selectpicker', 'data-live-search': 'true'}))
    price = forms.DecimalField(label='二次价格', max_digits=10, decimal_places=2,widget=forms.NumberInput(attrs={'class': 'form-control'}),required=False)
    amount = forms.IntegerField(label='数量', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    user = forms.ModelChoiceField(label='经手人', required=False, queryset=User.objects.all(),
                                  widget=forms.Select({'class': 'form-control'}))
    create_time = forms.CharField(label='创建时间', required=False, max_length=32,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))



class InorderForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False,
                            widget=forms.TextInput({'class': 'form-control', 'disabled': 'disabled'}))
    code = forms.CharField(label='入库单号', required=False, max_length=32,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    customer = forms.ModelChoiceField(label='部门', queryset=Department.objects.all(),widget=forms.Select({'class': 'form-control'}))
    user = forms.ModelChoiceField(label='经手人', required=False, queryset=User.objects.all(),
                                  widget=forms.Select({'class': 'form-control'}))
    create_time = forms.CharField(label='创建时间', required=False, max_length=32,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'disabled'}))


class InorderClothesForm(forms.Form):
    id = forms.IntegerField(label='ID', required=False,
                            widget=forms.TextInput({'class': 'form-control', 'disabled': 'disabled'}))
    outorder = forms.ModelChoiceField(label='入库单号', required=False, queryset=Inorder.objects.all(),
                                      widget=forms.Select({'class': 'form-control'}))
    clothes = forms.ModelChoiceField(label='器材信息', queryset=Clothes.objects.all(),
                                     widget=forms.Select({'class': 'selectpicker','data-live-search':'true'}))
    price = forms.ModelChoiceField(label='第二次价格', queryset=Clothes.objects.all(),
                                     widget=forms.Select({'class': 'selectpicker', 'data-live-search': 'true'}))

    amount = forms.IntegerField(label='数量', widget=forms.NumberInput(attrs={'class': 'form-control'}))


class EditmoreForm(forms.Form):
    clothes = forms.ModelChoiceField(label='器材', required=False, queryset=Clothes.objects.all(),
                                     widget=forms.Select({'class': 'form-control', 'disabled': 'disabled'}))
    amount = forms.IntegerField(label='数量', widget=forms.NumberInput(attrs={'class': 'form-control'}))
