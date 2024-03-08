from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, get_user_model
from django.views.generic import CreateView, DetailView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from users.forms import UserCreateForm, UserLoginForm


User = get_user_model()


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
            return redirect(reverse('products:index'))
            

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
            return redirect(reverse('products:index'))
        

class UserDetailView(DetailView):
    model = User
    template_name = 'users/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            """Redirects user to the index page if they are not logged in"""

            return super(UserDetailView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('products:index'))

    def get_object(self, queryset=None):
        return self.request.user

    

def logout_user(request):
    logout(request)
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    
    return redirect(reverse('products:index'))
