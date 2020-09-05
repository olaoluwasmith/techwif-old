from django.contrib import admin
from .models import *

# Register your models here.
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    prepopulated_fields = {'slug': ('category', )}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ['name', 'description', 'price', 'category']
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(ProductCategory, ProductCategoryAdmin)