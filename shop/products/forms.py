from django import forms

from products.models import Product

class ProductCreateForm(forms.ModelForm):
    """A form for updating an associate with the correct fields"""
        
    class Meta:
        model = Product
        fields = ('name', 'description', 'logo',
                  'price', 'count', 'category', 'holding')

        logo = forms.ImageField()

        # widgets = {
        #     'description': forms.Textarea(),
        # }

    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['logo'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['count'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['holding'].widget.attrs['class'] = 'form-control'

        self.fields['name'].required = True
        self.fields['description'].required = True
        self.fields['logo'].required = True
        self.fields['price'].required = True
        self.fields['count'].required = True
        self.fields['category'].required = True
        self.fields['holding'].required = True
