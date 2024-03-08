from django.urls import path

from .views import UserCreateView, UserLoginView, UserDetailView, logout_user

urlpatterns = [
    path(r'signup/', UserCreateView.as_view(), name='signup'),
    path(r'login/', UserLoginView.as_view(), name='login'),
    path(r'logout/', logout_user, name='logout')
]

urlpatterns += [
    path(r'profile/', UserDetailView.as_view(), name='profile')
]
