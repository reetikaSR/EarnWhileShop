from django import forms
from Shopping.models import Purchase


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['link', 'quantity', 'paytm_number']

    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)




