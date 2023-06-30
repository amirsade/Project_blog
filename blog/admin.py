from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status', 'categories']
    ordering = ('title', 'publish')
    list_filter = ['status', 'publish', 'author']
    search_fields = ('title', 'author')
    date_hierarchy = 'publish'
    list_display_links = ['author']
    list_editable = ['status']
    prepopulated_fields = {'slug': ['title']}


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email']


@admin.register(PostComment)
class CommentAdmin(admin.ModelAdmin):
    # list_display = '--all--'
    list_display = ['name', 'created', 'active', 'post']
    search_fields = ('text', 'name')
    list_filter = ['active', 'created', 'updated']
    list_editable = ['active']
    ordering = ('name', 'created')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    list_per_page = 10

