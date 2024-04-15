from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('products/', views.ProductList.as_view(), name='list_products'),
    path('create/', views.ProductCreate.as_view(), name='create_product'),
    path('update-product/<int:pk>/', views.ProductUpdate.as_view(), name='update_product'),
    path('delete-variant/<int:pk>/', views.delete_variant, name='delete_variant'),
]

