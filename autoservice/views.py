from django.shortcuts import render
from .models import Service, CarModel, Car, Order, OrderLine

def index(request):
    count_services = Service.objects.all().count()
    count_completed_orders = Order.objects.filter(status__exact="Finalized").count()
    count_cars = Car.objects.all().count()

    context = {
        'count_services': count_services,
        'count_completed_orders': count_completed_orders,
        'count_cars': count_cars
    }

    return render(request, 'index.html', context=context)