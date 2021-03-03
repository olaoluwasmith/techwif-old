from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    prepopulated_fields = {'slug': ('category', )}


class SectionAdmin(admin.ModelAdmin):
    list_display = ('section',)
    prepopulated_fields = {'slug': ('section', )}


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'modified_date')
    list_filter = ('created_date',)
    search_fields = ['title', 'content', 'author']
    prepopulated_fields = {'slug': ('title', )}


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'modified_date')
    list_filter = ('created_date',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title', )}


class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'modified_date')
    list_filter = ('created_date',)
    search_fields = ['title', 'content', 'author']
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Profile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(ForumComment)


# Changing the admin header
admin.site.site_header = "Olaoluwa Smith Technologies"
