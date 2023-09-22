from django.urls import path

from users.views import *


urlpatterns = [
    path('', UserListView.as_view(), name='list_user'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail_user'),
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='update_user'),
    path('delete/<int:pk>', UserDeleteView.as_view(), name='delete_user'),
    path('sendmail/', MessageSendCreateView.as_view(), name='message_send')
]


