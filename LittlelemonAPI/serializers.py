from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import MenuItem, Order, OrderItem, Cart

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id"]
        
class MenuItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"
        
class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        
class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
