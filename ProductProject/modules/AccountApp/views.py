from django.shortcuts import render,redirect
from django.views.generic import DetailView
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from modules.AccountApp.serializers import RegisterSerializer, UserListSerializer, UserSerializer, UserLoginSerializer, UserLogoutSerializer
import datetime
from rest_framework.response import Response
from rest_framework import status,permissions
from modules.ProductApiApp.models import Product
from modules.wishlistapiapp.models import WishItems

from django.contrib.auth.models import User

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

class Record(ListCreateAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Login(GenericAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)

        if serializer_class.is_valid(raise_exception=True):
            user = User.objects.get(username=serializer_class.data['user_id'])
            data = {
                'id' : user.id,
                'username':user.username,
                'email' : user.email,
                'is_staff' : user.is_staff,
                'token' : serializer_class.data['token']
            }
            return Response({'user':data}, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileDetailView(DetailView):
    """
    Displays the user profile of the logged in user.
    """
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'user_profile'

    def get(self, request, *args, **kwargs):
        context = {}
        if 'user' in self.request.session:
            user_profile = User.objects.get(username=self.request.session['user']['username'])
            context['user'] = user_profile
        return render(request, self.template_name,context)


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer
    template_name = 'account/signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request,*args,**kwargs):
        password = request.POST['password']
        password1 = request.POST['password1']
        if password == password1:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return redirect('productclientapp:login')

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
    permission_classes = (permissions.IsAuthenticated,)

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
    permission_classes = (permissions.IsAuthenticated,)

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
    permission_classes = (permissions.IsAuthenticated,)

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
    permission_classes = (permissions.IsAuthenticated,)

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