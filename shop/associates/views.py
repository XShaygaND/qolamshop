from django.views.generic import DetailView

from associates.models import Associate
from products.models import Product


class AssociateDetailView(DetailView):
    """Basic ListView for the Associate model"""
    
    model = Associate
    template_name = 'associates/details.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        associate = self.get_object()

        products = Product.objects.filter(owner=associate).order_by('-pub_date')
        data['product_list'] = products

        return data
