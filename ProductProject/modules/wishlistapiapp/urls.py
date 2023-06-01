from django.urls import path
from modules.wishlistapiapp import views

app_name = "wishlistapiapp"

urlpatterns = [
    path('create/', views.CreateWishItemsView.as_view(),name='wish_item_create'),
    path('list/', views.ListWishItemsView.as_view(),name='wish_item_list'),
    path('adminlist/', views.ListWishItemsAdminView.as_view(),name='wish_item_list_admin'),
    path('detail/<slug:slug>/', views.WishItemDetailView.as_view(),name='wish_item_detail'),
    path('delete/<slug:slug>/', views.WishItemDeleteView.as_view(),name='wish_item_delete'),
]