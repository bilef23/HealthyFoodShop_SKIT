from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")

    def __init__(self, *args, **kwargs):
        super(ProductForm,self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model=Product
        exclude=['user','code']

