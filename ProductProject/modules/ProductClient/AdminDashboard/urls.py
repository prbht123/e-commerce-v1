from django.urls import path
from modules.ProductClient.AdminDashboard import views

app_name = "admindashboard"

urlpatterns = [
   path('',views.AdminDashboardView.as_view(),name='home'),

   # users urls
   path('adminusers',views.AdminUsersListDashboardView.as_view(),name='admin_user_list'),
   path('normalusers',views.NormalUsersListDashboardView.as_view(),name='normal_user_list'),
   path('deactivatedusers',views.DeactivatedUsersListDashboardView.as_view(),name='deactivated_user_list'),
   path('modechangeusers/<int:pk>/',views.ModeChangeUserDashboardView.as_view(),name='mode_change_user'),

   # wishlist urls
   path('wishlists/',views.WishListDashboardView.as_view(),name='wish_lists'),
   path('wishlistdelete/<slug:slug>/',views.WishDeleteDashboardView.as_view(),name='wish_listt_delete'),

   # product urls
   path('productlist/',views.ProductListDashboardView.as_view(),name='product_list'),
   path('productdelete/<slug:slug>/',views.ProductDeleteDashboardView.as_view(),name='product_delete'),
   path('productcreate/',views.ProductCreateDashboardView.as_view(),name='product_create'),
]
