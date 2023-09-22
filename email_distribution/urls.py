from django.urls import path

from email_distribution.views import *


urlpatterns = [
    path('', EmailDistributionListView.as_view(), name='list'),
    path('<int:pk>/', EmailDistributionDetailView.as_view(), name='detail'),
    path('create/', EmailDistributionCreateView.as_view(), name='create'),
    path('update/<int:pk>', EmailDistributionUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', EmailDistributionDeleteView.as_view(), name='delete'),
    path('create_mail/', MessageCreateView.as_view(), name='create_mail')
]


