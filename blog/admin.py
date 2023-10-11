from django.contrib import admin

from blog.models import Blog
from pytils.translit import slugify


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'views')
    list_filter = ('created_at',)
    fields = ('title', 'description', 'image',)
    search_fields = ('title', 'description', )

    def save_model(self, request, obj, form, change):
        obj.slug = obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)

