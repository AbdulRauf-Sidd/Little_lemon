from django.urls import path
from . import views
from djoser.views import TokenCreateView
# Create your views here.
urlpatterns = [
    path('users', views.users),
    path('users/login', TokenCreateView.as_view(), name="token_create"),
    path('users/users/me', views.usersMe, name="token_create"),
    path('menu-items', views.menuItems),
    path('menu-items/<int:pk>', views.singleMenuItem),
    path('groups/managers/users', views.managers),
    path('groups/managers/users/<int:pk>', views.removeManager),
    path('groups/delivery-crew/users', views.deliveryCrew),
    path('groups/delivery-crew/users/<int:pk>', views.removeDeliveryCrew),
    path('cart/menu-items', views.cartItems),
    path('cart/menu-items/<int:pk>', views.singleMenuItem),
    path('orders', views.orders),
    path('orders/<int:pk>', views.singleOrder),
]