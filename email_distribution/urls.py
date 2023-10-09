from django.urls import path

from email_distribution.views import *

urlpatterns = [
    path('', EmailDistributionListView.as_view(), name='mailing_list'),
    path('<int:pk>/', EmailDistributionDetailView.as_view(), name='mailing_detail'),
    path('create/', EmailDistributionCreateView.as_view(), name='mailing_create'),
    path('update/<int:pk>', EmailDistributionUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>', EmailDistributionDeleteView.as_view(), name='mailing_delete'),
    path('create_mail/', MessageCreateView.as_view(), name='create_mail'),

    path('clients/', ClientListView.as_view(), name='clients_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('client/sendmail/', SendMessageCreateView.as_view(), name='send_message')
]
