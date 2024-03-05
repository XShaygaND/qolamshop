from django.urls import path

from .views import AssociateDetailView, AssociateUpdateView


urlpatterns = [
    path(r'associate/<slug:slug>', AssociateDetailView.as_view(), name='details'),
    path(r'associate/<slug:slug>/edit', AssociateUpdateView.as_view(), name='edit')
]
