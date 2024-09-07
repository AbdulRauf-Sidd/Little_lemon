from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .models import User, Group, MenuItem, Order, OrderItem, Cart
from . import serializers, helpers
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404 #return a friendly error response

@api_view(["POST"])
def users(request):
    """if request.method == "GET":
        users = get_list_or_404(User)
        serialized_data = serializers.UserSerializer(users, many=True)
        return Response({"users":serialized_data.data}, status.HTTP_200_OK)"""
    serialized = serializers.UserSerializer(data=request.data);
    if serialized.is_valid():
        serialized.save()
        return Response({"description": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def usersMe(request):
    user = request.user
    serialized = serializers.UserSerializer(user)
    return Response({"user": serialized.data}, status=status.HTTP_200_OK)

@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def managers(request):
    if helpers.manager_auth(request):
        if request.method == "GET":
            try:
                group = Group.objects.get(name='Manager')
                users_in_group = group.user_set.all()
                serialized_data = serializers.UserSerializer(users_in_group, many=True)
                return Response({'users': serialized_data.data}, status=status.HTTP_200_OK)
            except Group.DoesNotExist:
                return Response({'error': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if request.method == "POST":
            id = request.POST['id']
            user = get_object_or_404(User, id=id)
            user.groups.add("1")
            return Response({"description": "Added to manager"}, status.HTTP_201_CREATED);
    return Response(status=status.HTTP_401_UNAUTHORIZED)
   
    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def removeManager(request, pk):
    if helpers.manager_auth(request):
        user = get_object_or_404(User, id=pk);
        group = get_object_or_404(Group, name="Manager")
        user.groups.remove(group);
        return Response({"description":"Manager with user id " + str(pk) + " removed"}, status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    
@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deliveryCrew(request):
    if helpers.manager_auth(request):
        if request.method == "GET":
            try:
                group = Group.objects.get(name='Delivery_Crew')
                users_in_group = group.user_set.all()
                serialized_data = serializers.UserSerializer(users_in_group, many=True)
                return Response({'users': serialized_data.data}, status=status.HTTP_200_OK)
            except Group.DoesNotExist:
                return Response({'error': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if request.method == "POST":
            id = request.POST['id']
            user = get_object_or_404(User, id=id)
            group = get_object_or_404(Group, name="Delivery_Crew");
            user.groups.add(group)
            return Response({"description": "Added to Delivery Crew"}, status.HTTP_201_CREATED);
    return Response(status=status.HTTP_401_UNAUTHORIZED)    
    
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def removeDeliveryCrew(request, pk):
    if helpers.manager_auth(request):
        user = get_object_or_404(User, id=pk);
        group = get_object_or_404(Group, name="Delivery_Crew")
        user.groups.remove(group);
        return Response({"description":"Delivery Crew with user id " + str(pk) + " removed"}, status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def menuItems(request):
    if request.method == 'GET':
        if helpers.customer_auth(request) or helpers.manager_auth(request):
            paginator = PageNumberPagination()
            paginator.page_size = 10;
            items = get_list_or_404(MenuItem);
            items = paginator.paginate_queryset(items, request)
            serialized = serializers.MenuItemSerializers(items, many=True);
            return Response({"items": serialized.data}, status=status.HTTP_200_OK)
        return Response({"error":"not authenticated"}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'POST':
        if helpers.manager_auth(request):
            serialized = serializers.MenuItemSerializers(data=request.data);
            if serialized.is_valid():
                serialized.save();
                return Response({"description": "Item added successfully"}, status=status.HTTP_201_CREATED)
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"not authenticated"}, status=status.HTTP_403_FORBIDDEN)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def singleMenuItem(request, pk):
    if request.method == 'GET':
        if helpers.customer_auth(request) or helpers.manager_auth(request):
            items = get_object_or_404(MenuItem, id=pk);
            serialized = serializers.MenuItemSerializers(items);
            return Response({"items": serialized.data}, status=status.HTTP_200_OK)
        return Response({"error":"not authenticated"}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'PUT' or request.method == "PATCH":
        if helpers.manager_auth(request):
            item = get_object_or_404(MenuItem, id=pk)
            serialized = serializers.MenuItemSerializers(item, data=request.data);
            if serialized.is_valid():
                serialized.save();
                return Response({"description": "Item added successfully"}, status=status.HTTP_200_OK)
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"not authenticated"}, status=status.HTTP_403_FORBIDDEN)  
    if request.method == 'DELETE':
        if helpers.manager_auth(request):
            item = get_object_or_404(MenuItem, id=pk)
            item.delete()
            return Response({"Description":"Item with ID " + str(pk) + " Deleted"}, status=status.HTTP_200_OK)
        return Response({"error":"not authenticated"}, status=status.HTTP_403_FORBIDDEN)
    
    
    
@api_view(["GET", "POST", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cartItems(request):
    if helpers.customer_auth(request):
        user = request.user
        if request.method == 'GET':
            items = get_list_or_404(Cart, user=user);
            serialized = serializers.CartSerializers(items, many=True);
            return Response({"items": serialized.data}, status=status.HTTP_200_OK)
        
        if request.method == 'POST':
            serialized = serializers.CartSerializers(data=request.data)
            if serialized.is_valid():
                serialized.save();
                return Response({"items": serialized.data}, status=status.HTTP_201_CREATED);
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if request.method == 'DELETE':
            item = get_object_or_404(Cart, user = request.user)
            item.delete();
            return Response({"description": "Item deleted successfully"}, status=status.HTTP_200_OK)
    return Response({"error":"not authenticated"}, status=status.HTTP_403_FORBIDDEN)  

@api_view(["GET", "POST", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def orders(request):
    user = request.user
    crew = Group.objects.get(name='Delivery_Crew');
    manager = Group.objects.get(name='Manager');
    
    if request.method == 'GET':
        if len(user.groups.all()) == 0: #Customer
            order = get_object_or_404(Order, user=user);
            serialized = serializers.OrderSerializers(order);
            return Response({"order": serialized.data}, status=status.HTTP_200_OK)
        if crew in user.groups.all(): #Delivery Crew
            items = get_object_or_404(Order, delivery_crew=user);
            serialized = serializers.OrderSerializers(items);
            return Response({"order": serialized.data}, status=status.HTTP_200_OK)
        if helpers.manager_auth(request):
            order = get_list_or_404(Order);
            serialized = serializers.OrderSerializers(order, many=True);
            return Response({"order": serialized.data}, status=status.HTTP_200_OK)
        
    if request.method == 'POST':
        if len(user.groups.all()) == 0: #Customer
            serialized = serializers.OrderSerializers(data=request.data);
            if serialized.is_valid():
                serialized.save();
                return Response({"items": serialized.data}, status=status.HTTP_201_CREATED);
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error":"not authenticated"}, status=status.HTTP_403_FORBIDDEN)  

@api_view(["GET", "PATCH", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def singleOrder(request, pk):
    user = request.user
    crew = Group.objects.get(name='Delivery_Crew');
    manager = Group.objects.get(name='Manager');
    
    if request.method == 'GET':
        if len(user.groups.all()) == 0: #Customer
            order = get_object_or_404(Order, user=user, id=pk);
            serialized = serializers.OrderSerializers(order);
            return Response({"order": serialized.data}, status=status.HTTP_200_OK)
        return Response({"error":"not authenticated"}, status=status.HTTP_403_FORBIDDEN)  
    
    if request.method == 'PUT' or request.method == 'PATCH':
        
        if manager in user.groups.all(): #manager
            order = get_object_or_404(Order, id=pk);
            serialized = serializers.OrderSerializers(order, data=request.data, partial=True);
            if serialized.is_valid():
                serialized.save();
                return Response({"items": serialized.data}, status=status.HTTP_201_CREATED);
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == "PATCH" and crew in user.groups.all():
            order = get_object_or_404(Order, id=pk, delivery_crew = user);
            serialized = serializers.OrderSerializers(order, data=request.data, partial=True);
            if serialized.is_valid():
                serialized.save();
                return Response({"items": serialized.data}, status=status.HTTP_201_CREATED);
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"not authenticated"}, status=status.HTTP_403_FORBIDDEN)  
    