from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('store/', views.store, name="store"),
    path('store/<slug:slug>/<int:pk>/', views.ProductDetailView, name='product_detail'),
    path('store/categories/<category_slug>/', views.ProductCategoryView, name='product_category'),
    path('store_categories/', StoreCategory.as_view(), name='store_category'),
    path('store/<slug:slug>/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('store/<slug:slug>/<int:pk>/update_image/', views.ProductImageUpdate, name='product_update_image'),
    path('store/<slug:slug>/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product_form/', views.ProductCreateView, name='product_form'),

    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"), 

    path('store/amazon_products/', views.AmazonProducts, name='amazon_products'),   
]