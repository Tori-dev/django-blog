# from django.contrib import admin
# from .models import *


# # Register your models here.

# admin.site.register(Blog)
# admin.site.register(Category)
# admin.site.register(Comment)


from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Blog, Category, Comment

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ('title', 'author', 'category', 'date', 'status', 'Main_post')
    list_filter = ('category', 'date', 'status', 'Main_post')
    search_fields = ('title', 'content', 'author')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'category')
        }),
        ('Content', {
            'fields': ('content', 'image')
        }),
        ('Metadata', {
            'fields': ('status', 'Main_post')
        })
    )
    
    # Remove blog_slug from the editable fields
    exclude = ('blog_slug',)

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('name', 'email', 'post', 'date', 'parent')
    list_filter = ('date', 'post')
    search_fields = ('name', 'email', 'comment')
    
    fieldsets = (
        (None, {
            'fields': ('post', 'name', 'email')
        }),
        ('Comment Details', {
            'fields': ('comment', 'parent')
        }),
        ('Metadata', {
            'fields': ('date',)
        })
    )