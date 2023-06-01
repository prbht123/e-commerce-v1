from rest_framework import serializers
from modules.wishlistapiapp.models import WishItems
from modules.ProductApiApp.models import Product
from django.contrib.auth.models import User


class WishItemsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishItems
        fields = ['product', 'customer']

    def create(self, validated_data):
        try:
            wish_item = WishItems.objects.get(customer=validated_data['customer'],product = validated_data['product'])
            wish_item = wish_item.delete()
        except:
            wish_item = WishItems.objects.create(**validated_data)
        return wish_item



class WishItemsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishItems
        fields = ['id','slug','product', 'customer', 'quantity']