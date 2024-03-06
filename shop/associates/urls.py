from django.urls import path

from .views import AssociateDetailView, AssociateUpdateView, get_profile_or_associate


urlpatterns = [
    path(r'associate/get_profile', get_profile_or_associate, name='get_profile'),
    path(r'associate/<slug:slug>', AssociateDetailView.as_view(), name='details'),
    path(r'associate/<slug:slug>/edit', AssociateUpdateView.as_view(), name='edit')
]
