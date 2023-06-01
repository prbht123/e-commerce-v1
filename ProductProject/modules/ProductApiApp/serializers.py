from rest_framework import serializers
from modules.ProductApiApp.models import Product, Category


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'stock','image','image_url']

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product



class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','slug','name', 'price', 'category', 'description', 'stock','image','image_url']