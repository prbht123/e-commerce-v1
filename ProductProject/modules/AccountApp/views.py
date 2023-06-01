from django.shortcuts import render,redirect
from django.views.generic import DetailView
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from modules.AccountApp.serializers import RegisterSerializer, UserListSerializer
import datetime
from rest_framework.response import Response
from rest_framework import status
from modules.ProductApiApp.models import Product
from modules.wishlistapiapp.models import WishItems
# Create your views here.

success_response = {
    'data':{},
    'is_success':True,
    'error_code':0,
    'error_message':"",
}

error_response = {
    'data':{},
    'error_code':0,
    'error_message':"",
    'is_success':False
}


class ProfileDetailView(DetailView):
    """
    Displays the user profile of the logged in user.
    """
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'user_profile'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    template_name = 'account/signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request,*args,**kwargs):
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return redirect('accountapp:login')

        return render(request, self.template_name)


class UserProductCountView(GenericAPIView):
    serializer_class = UserListSerializer
    def get(self, request):
        try:
            date_from = datetime.datetime.now() - datetime.timedelta(days=1)
            month_from = datetime.datetime.now() - datetime.timedelta(days=30)
            
            total_users = User.objects.count()
            last_day_count_users = User.objects.filter(
                date_joined__gte=date_from).count()
            last_month_count_users = User.objects.filter(
                date_joined__gte=month_from).count()

            total_products = Product.objects.count()
            last_day_count_product = Product.objects.filter(
                date_created__gte=date_from).count()
            last_month_count_product = Product.objects.filter(
                date_created__gte=month_from).count()

            total_wish_users = WishItems.objects.count()
            last_day_count_wish_list = WishItems.objects.filter(
                date_created__gte=date_from).count()
            last_month_count_wish_list = WishItems.objects.filter(
                date_created__gte=month_from).count()

            context = {
                'total_users': total_users,
                'last_day_count_users': last_day_count_users,
                'last_month_count_users': last_month_count_users,
                'total_products': total_products,
                'last_day_count_product': last_day_count_product,
                'last_month_count_product': last_month_count_product,
                'total_wish_users':total_wish_users,
                'last_day_count_wish_list':last_day_count_wish_list,
                'last_month_count_wish_list':last_month_count_wish_list
            }
            success_response.update(data = context)
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message="Products and Users errors")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST) 

class AdminUserListView(GenericAPIView):
    serializer_class = UserListSerializer
    def get(self, request):
        try:
            queryset = User.objects.filter(is_staff = True,is_active=True).order_by('first_name','last_name')
            serializer = UserListSerializer(queryset,many=True)
            success_response.update(data = serializer.data)
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message="No admin Users")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST) 

class NormalUserListView(GenericAPIView):
    serializer_class = UserListSerializer
    def get(self, request):
        try:
            queryset = User.objects.filter(is_active=True,is_staff=False).order_by('first_name','last_name')
            serializer = UserListSerializer(queryset,many=True)
            success_response.update(data = serializer.data)
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message="No normal users")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST) 

class DeactivatedUserListView(GenericAPIView):
    serializer_class = UserListSerializer
    def get(self, request):
        try:
            queryset = User.objects.filter(is_active=False).order_by('first_name','last_name')
            serializer = UserListSerializer(queryset,many=True)
            success_response.update(data = serializer.data)
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message="No Deactiaved Users")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST) 


class ChangeModeUserView(GenericAPIView):
    serializer_class = UserListSerializer
    def get(self, request,pk, *args, **kwargs):
        mode = self.request.GET.get('mode',None)
        try:
            user = User.objects.get(id=pk)
            if mode == 'staff':
                user.is_staff = True
            if mode == 'normaluser':
                user.is_staff = False
            if mode == 'activate':
                user.is_active = True
            if mode == 'deactivate':
                user.is_active = False
                user.is_staff = False
            user.save()
            success_response.update(data = "Successfully mode chnaged.")
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message="No user found")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST) 