from .models import User, Group

def manager_auth(request):
    user = request.user;
    group = Group.objects.get(name='Manager')
    return user.is_superuser or group in user.groups.all();

def customer_auth(request):
    user = request.user;
    group = Group.objects.get(name='Delivery_Crew');
    return len(user.groups.all()) == 0 or group in user.groups.all();