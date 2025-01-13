# forms.py
from django import forms
from order.models import ShippingAddress
from customer.models import Customer

class AddressSelectionForm(forms.Form):
    address = forms.ModelChoiceField(
        queryset=Customer.objects.none(),
        required=False,
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['address'].queryset = Customer.objects.filter(user=user)

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'