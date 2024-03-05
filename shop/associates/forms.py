from django import forms

from associates.models import Associate

class AssociateUpdateForm(forms.ModelForm):
    """A form for updating an associate with the correct fields"""
        
    class Meta:
        model = Associate
        fields = ('description', 'logo', 'website')

        logo = forms.ImageField()
        website=forms.URLField()

        widgets = {
            'description': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super(AssociateUpdateForm, self).__init__(*args, **kwargs)

        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['logo'].widget.attrs['class'] = 'form-control'
        self.fields['website'].widget.attrs['class'] = 'form-control'

        self.fields['website'].required = True
