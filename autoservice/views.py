from django.contrib.admindocs.views import BookmarkletsView
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Service, CarModel, Car, Order, OrderLine
from django.shortcuts import render, get_object_or_404
from django.views import generic

def index(request):
    count_services = Service.objects.all().count()
    count_completed_orders = Order.objects.filter(status__exact="Finalized").count()
    count_cars = Car.objects.all().count()
    count_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = count_visits + 1
    context = {
        'count_services': count_services,
        'count_completed_orders': count_completed_orders,
        'count_cars': count_cars,
        'count_visits': count_visits
    }

    return render(request, 'index.html', context=context)

def cars(request):
    paginator = Paginator(Car.objects.all(), 2)
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)
    context = {
        'cars': cars
    }
    return render(request, 'cars.html', context=context)

def search(request):
    query = request.GET.get('query')
    search_results = Car.objects.filter(Q(national_id__icontains=query) | Q(car_model_ID__make__icontains=query)
                                        | Q(VIN_code__icontains=query) | Q(client__icontains=query) | Q(car_model_ID__model__icontains=query))
    return render(request, 'search.html', {'cars': search_results, 'query': query})

def car(request, national_id):
    single_car = get_object_or_404(Car, pk=national_id)
    return render(request, 'car.html', {'car':single_car})

class OrdersView(generic.ListView):
    model = Order
    paginate_by = 1
    template_name = 'order_list.html'

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'

