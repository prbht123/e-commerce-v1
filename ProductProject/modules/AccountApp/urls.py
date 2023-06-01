from django.urls import path
from modules.AccountApp import views
# from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = "accountapp"

urlpatterns = [
    path('registration', views.RegisterView.as_view(),name='registration'),
   path('login/', auth_views.LoginView.as_view(template_name='account/signin.html'), name="login"),
   path('logout/', auth_views.LogoutView.as_view(template_name='account/signout.html'), name='logout'),
   path('password-reset/', auth_views.PasswordResetView.as_view(template_name='account/registration/password_reset_form.html',
         subject_template_name='account/registration/password_reset_subject.txt', email_template_name='account/registration/password_reset_email.html', success_url=reverse_lazy('accountapp:password_reset_done')), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/registration/password_reset_confirm.html',success_url=reverse_lazy('accountapp:login')), name='password_reset_confirm'),
   path('profile/', views.ProfileDetailView.as_view(), name='profile'),


   # api enduser
   path('countuserproduct/',views.UserProductCountView.as_view(),name='count_user_product'),
   path('adminusers/',views.AdminUserListView.as_view(),name='admin_users'),
   path('normalusers/',views.NormalUserListView.as_view(),name='normal_users'),
   path('deactivatedusers/',views.DeactivatedUserListView.as_view(),name='deactivated_users_list'),
   path('changemodeuser/<int:pk>/',views.ChangeModeUserView.as_view(),name='changemode_user'),

]
