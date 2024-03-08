from django.views.generic import DetailView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse

from associates.models import Associate
from associates.forms import AssociateUpdateForm
from products.models import Product


class AssociateDetailView(DetailView):
    """DetailView for viewing the information about an associate"""
    
    model = Associate
    template_name = 'associates/details.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        associate = self.get_object()

        products = Product.objects.filter(owner=associate).order_by('-pub_date')
        data['product_list'] = products

        return data


class AssociateUpdateView(UpdateView):
    """UpdateView for associates to update their information"""

    model = Associate
    template_name = 'associates/update.html'
    form_class = AssociateUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            """Redirects user to the index page if they are not logged in or not the original associate"""

            return redirect(reverse('associates:details', args=args, kwargs=kwargs))
        
        elif self.get_object().owner != request.user:
            return redirect(reverse('associates:details', args=args, kwargs=kwargs))
            
        else:
            return super(AssociateUpdateView, self).dispatch(request, *args, **kwargs)
        

def get_profile_or_associate(request):
    if request.user.is_associate:
        return redirect('associates:details', Associate.objects.get(owner=request.user).slug)
    
    return redirect('users:profile') # TODO: Create profile page


# class AssociateStatsDetailView(DetailView):
#     """A view for viewing the stats of an associate"""

# TODO: Create a view for viewing the stats of an associate
        
#     model = Associate
#     template_name = ''
