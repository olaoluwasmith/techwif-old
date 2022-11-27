from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    prepopulated_fields = {'slug': ('category', )}


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'modified_date')
    list_filter = ('created_date',)
    search_fields = ['title', 'content', 'author']
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Profile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)


# Changing the admin header
admin.site.site_header = "TechWif"
