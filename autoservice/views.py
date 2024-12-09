from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin

from .forms import OrderReviewForm, UserUpdateForm, ProfileUpdateForm
from .models import Service, CarModel, Car, Order, OrderLine
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required

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
    paginate_by = 2
    template_name = 'order_list.html'


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'order_detail.html'
    form_class = OrderReviewForm

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)

class OrdersByUsersListView(LoginRequiredMixin,generic.ListView):
    model = Order
    template_name = 'user_orders.html'
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).filter(status__exact="Pending").order_by('deadline')

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 =request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} is taken! Try not to be as mainstream ;)')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User with this email address already exist')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User {username} has been registered. You can finally use our services!!')
                    return redirect('login')
        else:
            messages.error(request, f'Passwords does not match')
            return redirect('register')
    return render(request, 'register.html')

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile was updated successfully')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'profile.html', context)