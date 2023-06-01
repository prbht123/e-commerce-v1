from django.urls import path
from modules.ProductClient.ClientApp import views

app_name = "productclientapp"

urlpatterns = [
   path('',views.HomeView.as_view(),name='home'),
   path('aboutus/',views.AboutUsView.as_view(),name='about_us'),
   path('contact/',views.ContactView.as_view(),name='contact'),
   path('productlist/',views.ProductListView.as_view(),name='list_product'),
   path('productdetail/<slug:slug>/',views.ProductDetailView.as_view(),name='detail_product'),
   path('createwishitem/', views.CreateWishItemsView.as_view(),name='create_wish_item'),
   path('listwishitem/', views.ListWishItemsView.as_view(),name='list_wish_item'),
]
