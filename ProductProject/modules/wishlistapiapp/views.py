from django.shortcuts import render
from modules.wishlistapiapp.serializers import WishItemsCreateSerializer,WishItemsListSerializer
from modules.ProductApiApp.serializers import ProductListSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status,permissions
from modules.ProductApiApp.models import Product
from modules.wishlistapiapp.models import WishItems
from modules.AccountApp.serializers import UserListSerializer
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


class CreateWishItemsView(GenericAPIView):
    serializer_class = WishItemsCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            serializer = WishItemsCreateSerializer(data=request.data)
            if serializer.is_valid():
                product = serializer.save()
                success_response.update(data = {"message":"Wish items added successfully..."})
                return Response(success_response, status=status.HTTP_201_CREATED)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message=serializer.errors)
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

class ListWishItemsView(GenericAPIView):
    serializer_class = WishItemsListSerializer
    
    def get(self, request):
        try:
            user_id = self.request.GET.get('user_id',None)
            if user_id:
                queryset = WishItems.objects.filter(customer__id = int(user_id))
            else:
                queryset = WishItems.objects.all()
            serializer = WishItemsListSerializer(queryset,many=True)
            products = [int(x['product']) for x in serializer.data]
            wish_products = Product.objects.filter(id__in = products)
            serializer = ProductListSerializer(wish_products,many=True)
            success_response.update(data = serializer.data)
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message=serializer.errors)
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

class WishItemDetailView(GenericAPIView):
    serializer_class = WishItemsListSerializer
    queryset = WishItems.objects.all()
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request,*args,**kwargs):
        try:
            instance = self.get_object()
            serializer = WishItemsListSerializer(instance)
            success_response.update(data = serializer.data)
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message="Wish items Not Available")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST) 

class WishItemDeleteView(GenericAPIView):
    serializer_class = WishItemsListSerializer
    queryset = WishItems.objects.all()
    lookup_field = 'slug'
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request,*args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            success_response.update(data = "successfully deleted...")
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message="Wish items Not Available")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST) 

class ListWishItemsAdminView(GenericAPIView):
    serializer_class = WishItemsListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            queryset = WishItems.objects.all()
            wish_list_information = []
            for item in queryset:
                product = ProductListSerializer(item.product)
                user = UserListSerializer(item.customer)
                data = {
                    'wish_list_slug' : item.slug,
                    'user' : user.data['first_name'] + ' ' + user.data['last_name'],
                    'product' : product.data
                }

                wish_list_information.append(data)
            
            success_response.update(data = wish_list_information)
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message="serializer.errors")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)