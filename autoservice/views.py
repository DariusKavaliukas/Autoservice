from django.contrib.admindocs.views import BookmarkletsView

from .models import Service, CarModel, Car, Order, OrderLine
from django.shortcuts import render, get_object_or_404
from django.views import generic

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

def cars(request):
    cars = Car.objects.all()
    context = {
        'cars': cars
    }
    return render(request, 'cars.html', context=context)

def car(request, national_id):
    single_car = get_object_or_404(Car, pk=national_id)
    return render(request, 'car.html', {'car':single_car})

class OrdersView(generic.ListView):
    model = Order
    template_name = 'order_list.html'

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'