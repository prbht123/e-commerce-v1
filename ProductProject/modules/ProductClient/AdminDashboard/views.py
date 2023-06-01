from django.shortcuts import render,redirect
from django.views import View
import requests
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

import json
from rest_framework.authtoken.models import Token

# Create your views here.


class AdminDashboardView(View):
    def get(self,request,*args,**kwargs):
        end_url = 'http://127.0.0.1:8000/account/countuserproduct/' 
        products = requests.get(end_url)
        context = products.json()['data']
        return render(request,'admindashboard/dashboard.html',context)

class AdminUsersListDashboardView(View):
    paginate_by = 5

    def get(self,request,*args,**kwargs):
        if 'user' in self.request.session and self.request.session['user']['is_staff']:
            auth_token = self.request.session['user']['token']
            headers = {'Authorization': f'Token {auth_token}'}
            end_url = 'http://127.0.0.1:8000/account/adminusers/' 
            products = requests.get(end_url,headers=headers)
            context = {
                'admin_users' : products.json()['data']
            }

            paginator = Paginator(context['admin_users'],self.paginate_by)
            page = self.request.GET.get('page')
            try:
                admin_user = paginator.page(page)
            except PageNotAnInteger:
                admin_user = paginator.page(1)
            except EmptyPage:
                admin_user = paginator.page(paginator.num_pages)  
            context['admin_users'] = admin_user

            return render(request,'admindashboard/users/adminusers.html',context)
        
        return redirect('admindashboard:home')

class NormalUsersListDashboardView(View):
    paginate_by = 5

    def get(self,request,*args,**kwargs):
        if 'user' in self.request.session and self.request.session['user']['is_staff']:
            auth_token = self.request.session['user']['token']
            headers = {'Authorization': f'Token {auth_token}'}
            end_url = 'http://127.0.0.1:8000/account/normalusers/' 
            products = requests.get(end_url,headers=headers)
            context = {
                'normal_users' : products.json()['data']
            }

            paginator = Paginator(context['normal_users'],self.paginate_by)
            page = self.request.GET.get('page')
            try:
                normal_user = paginator.page(page)
            except PageNotAnInteger:
                normal_user = paginator.page(1)
            except EmptyPage:
                normal_user = paginator.page(paginator.num_pages)  
            context['normal_users'] = normal_user

            return render(request,'admindashboard/users/normalusers.html',context)

        return redirect('admindashboard:home')

class DeactivatedUsersListDashboardView(View):
    paginate_by = 5

    def get(self,request,*args,**kwargs):
        if 'user' in self.request.session and self.request.session['user']['is_staff']:
            auth_token = self.request.session['user']['token']
            headers = {'Authorization': f'Token {auth_token}'}
            end_url = 'http://127.0.0.1:8000/account/deactivatedusers/' 
            products = requests.get(end_url,headers=headers)
            context = {
                'deactivate_users' : products.json()['data']
            } 
            paginator = Paginator(context['deactivate_users'],self.paginate_by)
            page = self.request.GET.get('page')
            try:
                deactivate_user = paginator.page(page)
            except PageNotAnInteger:
                deactivate_user = paginator.page(1)
            except EmptyPage:
                deactivate_user = paginator.page(paginator.num_pages)  
            context['deactivate_users'] = deactivate_user

            return render(request,'admindashboard/users/deactivatedusers.html',context)

        return redirect('admindashboard:home')
        

class ModeChangeUserDashboardView(View):
    def get(self,request,pk,*args,**kwargs):
        if 'user' in self.request.session and self.request.session['user']['is_staff']:
            auth_token = self.request.session['user']['token']
            headers = {'Authorization': f'Token {auth_token}'}
            mode = self.request.GET.get('mode',None)
            end_url = 'http://127.0.0.1:8000/account/changemodeuser/' +str(pk)+'?mode='+mode
            products = requests.get(end_url,headers=headers)
            context = products.json()
            if mode == 'deactivate' or mode == 'staff':
                return redirect('admindashboard:normal_user_list')
            if mode == 'activate':
                return redirect('admindashboard:deactivated_user_list')
            if mode == 'normaluser':
                return redirect('admindashboard:admin_user_list')

        return redirect('admindashboard:home')


class WishListDashboardView(View):
    paginate_by = 5

    def get(self,request,*args,**kwargs):
        if 'user' in self.request.session:
            context = {}
            auth_token = self.request.session['user']['token']
            headers = {'Authorization': f'Token {auth_token}'}
            end_url = end_url = 'http://127.0.0.1:8000/wishlist/adminlist/' 
            wish_items = requests.get(end_url,headers=headers)
            if wish_items:
                context['wish_items'] =  wish_items.json()['data']
                

                paginator = Paginator(context['wish_items'],self.paginate_by)
                page = self.request.GET.get('page')
                try:
                    wish_item = paginator.page(page)
                except PageNotAnInteger:
                    wish_item = paginator.page(1)
                except EmptyPage:
                    wish_item = paginator.page(paginator.num_pages)  
                context['wish_items'] = wish_item
        return render(request,'admindashboard/wishlist/adminwishlist.html',context)

class WishDeleteDashboardView(View):
    def get(self,request,slug,*args,**kwargs):
        if 'user' in self.request.session:
            auth_token = self.request.session['user']['token']
            headers = {'Authorization': f'Token {auth_token}'}
            end_url = end_url = 'http://127.0.0.1:8000/wishlist/delete/' + slug + '/'
            wish_items = requests.delete(end_url,headers=headers)
            context = {
                'wish_items':wish_items.json()
            }

        return redirect('admindashboard:wish_lists')


class ProductListDashboardView(View):
    paginate_by = 5

    def get(self,request,*args,**kwargs):
        context = {}
        end_url = end_url = 'http://127.0.0.1:8000/products/list/'
        products = requests.get(end_url)
        if products:
            context = {
                'products':products.json()['data']
            }
            paginator = Paginator(context['products'],self.paginate_by)
            page = self.request.GET.get('page')
            try:
                product = paginator.page(page)
            except PageNotAnInteger:
                product = paginator.page(1)
            except EmptyPage:
                product = paginator.page(paginator.num_pages)  
                
            context['products'] = product
        return render(request,'admindashboard/product/list.html',context)

class ProductDeleteDashboardView(View):
    def get(self,request,slug,*args,**kwargs):
        if 'user' in self.request.session:
            auth_token = self.request.session['user']['token']
            headers = {'Authorization': f'Token {auth_token}'}
            end_url = end_url = 'http://127.0.0.1:8000/products/delete/' + slug + '/'
            products = requests.delete(end_url, headers=headers)
        return redirect('admindashboard:product_list')

class ProductCreateDashboardView(View):
    def get(self,request,*args,**kwargs): 
        print("66666666666666666666666") 
        if 'user' in self.request.session:
            print("4444444444444444444")
            auth_token = self.request.session['user']['token']
            headers = {'Authorization': f'Token {auth_token}'}
            dummy = json.loads(open("dummydata.json","rb").read())
            end_url = 'http://127.0.0.1:8000/products/create/'
            for d in dummy:
                data = {
                    'image_url' : d['image'],
                    'name' : d['name'],
                    'price' : d['price'],
                    'stock' : d['stock'],
                    'description' : d['description'],
                    'category' : d['category']
                }
                products = requests.post(end_url,headers=headers, data= data)
        return redirect('admindashboard:product_list')

class CalenderDashboardView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'admindashboard/calender/admincalender.html')

class MapsDashboardView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'admindashboard/maps.html')
