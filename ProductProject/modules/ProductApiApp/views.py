from django.shortcuts import render
from modules.ProductApiApp.serializers import ProductCreateSerializer,ProductListSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from modules.ProductApiApp.models import Product, Category
import base64

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


class CreateProductView(GenericAPIView):
    serializer_class = ProductCreateSerializer
    def post(self, request):
        try:
            try:
                category = Category.objects.get(name=request.data['category'])
        
            except:
                category = Category.objects.create(name=request.data['category'])

            data = {
                'image_url' : request.data['image_url'],
                'name' : request.data['name'],
                'price' : request.data['price'],
                'stock' : request.data['stock'],
                'description' : request.data['description'],
                'category' : category.id
            }

            serializer = ProductCreateSerializer(data=data)
            if serializer.is_valid():
                product = serializer.save()

                success_response.update(data = {"message":"Product added successfully..."})
                return Response(success_response, status=status.HTTP_201_CREATED)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message=serializer.errors)
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(GenericAPIView):
    serializer_class = ProductListSerializer
    def get(self, request):
        try:
            # queryset = Product.objects.all().order_by('name')
            queryset = Product.objects.prefetch_related('wish_product').all().order_by('name')
            serializer = ProductListSerializer(queryset,many=True)
            success_response.update(data = serializer.data)
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message="Products Not Available")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)      

class ProductDetailView(GenericAPIView):
    serializer_class = ProductListSerializer
    def get(self, request,slug):
        try:
            queryset = Product.objects.get(slug=slug)
            serializer = ProductListSerializer(queryset)
            success_response.update(data = serializer.data)
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message="Product Not Available")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST) 

class ProductDeleteView(GenericAPIView):
    def delete(self, request, slug, format= None):
        try:
            queryset = Product.objects.get(slug = slug)
            queryset.delete()
            success_response.update(data = {"message":"Product Deleted Successfully"})
            return Response(success_response, status=status.HTTP_201_CREATED)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message= "Product Not Found")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

class ProductNameListView(GenericAPIView):
    serializer_class = ProductListSerializer
    def get(self, request,name):
        try:
            queryset = Product.objects.filter(name__icontains=name).order_by('name')
            serializer = ProductListSerializer(queryset,many=True)
            success_response.update(data = serializer.data)
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message="Products Not Available")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)      

class ProductCategoryWiseListView(GenericAPIView):
    serializer_class = ProductListSerializer
    def get(self, request):
        try:
            category_products_list = []
            category_list = Category.objects.all()
            for category in category_list:
                print(category)
                products = Product.objects.filter(category = category).order_by('name')
                serializer = ProductListSerializer(products,many=True)
                data = {
                    'category' : category.name,
                    'products'  : serializer.data
                }
                category_products_list.append(data)   
            success_response.update(data = category_products_list)
            return Response(success_response, status=status.HTTP_200_OK)
        except:
            error_response.update(error_code=status.HTTP_400_BAD_REQUEST,error_message="Products Not Available")
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST) 