from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from users.forms import UserCreateForm, UserLoginForm


class UserCreateView(CreateView):
    """Basic CreateView for creating a new user"""

    form_class = UserCreateForm
    template_name = "auth/signup.html"
    success_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        """Redirects user to the index page if they are logged in"""

        if request.user.is_anonymous:
            return super(UserCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('products:index'))
            

class UserLoginView(LoginView):
    """A modified view that inherits from django.contrib.auth.views.LoginView"""
    
    form_class = UserLoginForm
    template_name = "auth/login.html"
    success_url = reverse_lazy('products:index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            """Redirects user to the index page if they are logged in"""

            return super(UserLoginView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('products:index'))
    

def logout_user(request):
    logout(request)
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    
    return redirect('products:index')
