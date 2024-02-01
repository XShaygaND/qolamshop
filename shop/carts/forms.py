from django import forms

from carts.models import Order

class OrderCreateForm(forms.ModelForm):
    """A form that has it's fields are bootstrapified and first and last name and email field are required"""
        
    class Meta:
        model = Order
        fields = ('address', 'phone', 'postal_code', 'delivery_method')

        widgets = {
            'address': forms.Textarea(),
            'phone': forms.NumberInput(),
            'postal_code': forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['postal_code'].widget.attrs['class'] = 'form-control'
        self.fields['delivery_method'].widget.attrs['class'] = 'form-control'

        self.fields['address'].required = True
        self.fields['phone'].required = True
        self.fields['postal_code'].required = True
