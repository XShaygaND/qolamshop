from django.urls import path

from .views import AssociateDetailView


urlpatterns = [
    path(r'a/<slug:slug>', AssociateDetailView.as_view(), name='details')
]