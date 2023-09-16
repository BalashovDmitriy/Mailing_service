from django.urls import path

from email_distribution.views import IndexTemplateView


urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
]


