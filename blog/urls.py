from django.urls import path

from blog.views import BlogDetailView

urlpatterns = [
    path('<slug>', BlogDetailView.as_view(), name='blog_detail'),
]
