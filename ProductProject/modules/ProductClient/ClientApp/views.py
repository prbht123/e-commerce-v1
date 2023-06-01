from django.shortcuts import render,redirect
from django.views import View
import requests
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from modules.ProductClient.cartapp.forms import CartAddProductForm
from django.core.paginator import *

# Create your views here.


class HomeView(View):
    def get(self,request,*args,**kwargs):
        context = {}
        end_url = 'http://127.0.0.1:8000/products/categoryproductlist/'
        context['category_products_list'] = requests.get(end_url).json()['data']
        context['cart_product_form'] = CartAddProductForm()
        if self.request.user.id:
            end_url = 'http://127.0.0.1:8000/wishlist/list/' + '?user_id=' + str(self.request.user.id)
            context['wish_list'] = requests.get(end_url).json()['data']
            context['wish_list'] = [x['id'] for x in context['wish_list']]
            
        return render(request,'client/home.html',context)

class AboutUsView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'client/aboutus.html')

class ContactView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'client/contact.html')


class ProductListView(View):
    paginate_by = 5

    def get(self,request,*args,**kwargs):
        product_name = self.request.GET.get('product')
        context = {}
        if product_name:
            end_url = 'http://127.0.0.1:8000/products/namelist/' + product_name + '/'
        else:
            end_url = 'http://127.0.0.1:8000/products/list/'

        products = requests.get(end_url)
        context['products'] = products.json()['data']
        if self.request.user.id:
            end_url = 'http://127.0.0.1:8000/wishlist/list/' + '?user_id=' + str(self.request.user.id)
            context['wish_list'] = requests.get(end_url).json()['data']
            context['wish_list'] = [x['id'] for x in context['wish_list']]

        context['cart_product_form'] = CartAddProductForm()

        paginator = Paginator(context['products'],self.paginate_by)
        page = self.request.GET.get('page')
        try:
            product = paginator.page(page)
        except PageNotAnInteger:
            product = paginator.page(1)
        except EmptyPage:
            product = paginator.page(paginator.num_pages)  
              
        context['products'] = product
        return render(request,'client/products/list.html',context)

class ProductDetailView(View):
    def get(self,request,*args,**kwargs):
        slug = kwargs['slug']
        context = {}
        if slug:
            end_url = 'http://127.0.0.1:8000/products/detail/' + slug + '/'
            products = requests.get(end_url)
            print(products.json()['data'])
            context['product'] = products.json()['data']
            context['cart_product_form'] = CartAddProductForm()
            return render(request,'client/products/detail.html',context)

class CreateWishItemsView(View):
    def get(self,request,*args,**kwargs):
        end_url = 'http://127.0.0.1:8000/wishlist/create/' 
        customer = self.request.user.id
        product = self.request.GET.get('product_id',None)
        data = {
            'customer':customer,
            'product' : product,
        }
        products = requests.post(end_url,data=data)
        context = products.json()
        return redirect('productclientapp:list_product')

class ListWishItemsView(View):
    def get(self,request,*args,**kwargs):
        end_url = end_url = 'http://127.0.0.1:8000/wishlist/list/' + '?user_id=' + str(self.request.user.id) 
        wish_items = requests.get(end_url)
        context = {
            'wish_items':wish_items.json()['data']
        }
        return render(request,'wishlist/clientlist.html',context)

