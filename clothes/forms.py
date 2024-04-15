from django import forms


class ClothesForm(forms.Form):
    lei_choices = (
        (1, "一类"),
        (2, "二类"),
        (3, "三类"),
    )
    lei = forms.ChoiceField(label='类别', choices=lei_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    danwei_choices = (
        (1, "台"),
        (2, "套"),
        (3, "件"),
        (4, "个"),
        (5, "盒"),
        (6, "箱"),
        (7, "斤"),
    )
    id = forms.IntegerField(label='ID', required=False,
                            widget=forms.TextInput({'class': 'form-control', 'disabled': 'disabled'}))
    name = forms.CharField(label='机件名', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sn = forms.CharField(label='机件号', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label='价格', max_digits=10, decimal_places=3,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    danwei = forms.ChoiceField(label='单位', choices=danwei_choices, widget=forms.Select(attrs={'class': 'form-control'}))

    stock = forms.IntegerField(label='库存', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    stock_down = forms.IntegerField(label='最低库存', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label='图片', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    desc = forms.CharField(label='描述', required=False, max_length=200,
                           widget=forms.Textarea(attrs={'class': 'form-control'}))
    changjia = forms.CharField(label='厂家', required=False, max_length=200,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))