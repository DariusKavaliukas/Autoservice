from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("cars/", views.cars, name='cars'),
    path('cars/<int:national_id>', views.car, name='car'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('search/', views.search, name='search'),
    path('myorders/', views.OrdersByUsersListView.as_view(), name='my-orders'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]

