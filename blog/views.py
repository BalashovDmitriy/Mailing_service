
from django.views.generic import DetailView

from blog.models import Blog


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        obj.views += 1
        obj.save()
        return obj
