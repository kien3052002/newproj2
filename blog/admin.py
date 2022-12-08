from django.contrib import admin
from . import models

from django.db.models import Q


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('Title', 'status', 'Slug', 'author')
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('Content', 'Post', 'name', 'publish', 'post_author')
    list_filter = ('publish', 'post')
    search_fields = ('name', 'content')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(name=request.user) | qs.filter(post_author=request.user)


admin.site.register(models.Category)
