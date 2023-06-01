from django.urls import path
from modules.ProductApiApp import views

app_name = "productapiapp"

urlpatterns = [
   path('create/', views.CreateProductView.as_view(),name='product_create'),
   path('list/', views.ProductListView.as_view(),name='product_list'),
   path('detail/<slug:slug>/', views.ProductDetailView.as_view(),name='product_detail'),
   path('delete/<slug:slug>/', views.ProductDeleteView.as_view(),name='product_delete'),
   path('namelist/<str:name>/',views.ProductNameListView.as_view(),name='product_name_list'),
   
   path('categoryproductlist/', views.ProductCategoryWiseListView.as_view(),name='category_product_list'),
]
