from django import forms
from deal.models import Deal

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['subject','price','content']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'price': forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'subject':'상품',
            'price':'가격',
            'content':'설명'
        }