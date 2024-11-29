from django.db import models
from datetime import datetime
import uuid

from django.db.models import PROTECT


class Service(models.Model):
    name = models.CharField('Service', max_length=200, help_text='Enter service name (e.g., Change oil)')
    price = models.FloatField("Price", help_text='Enter service price')

    def __str__(self):
        return f'{self.name} {self.price}'

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'



class CarModel(models.Model):
    make = models.CharField(max_length=50, help_text='Enter car make')
    model = models.CharField(max_length=50, help_text='Enter car model')
    year = models.CharField(max_length=4, null=True, help_text='Enter car year')
    engine = models.CharField(max_length=50, null=True, help_text='Enter car engine')

    def __str__(self):
        return f'{self.make} {self.model} {self.engine}'

    class Meta:
        verbose_name = 'Car model'
        verbose_name_plural = 'Car models'

class Car(models.Model):
    national_id = models.CharField('National number', max_length=20, help_text="Car plate")
    car_model_ID = models.ForeignKey('CarModel', on_delete=models.SET_NULL, null=True)
    VIN_code = models.CharField('VIN code', max_length=17,
        help_text='17 characters unique number, more: <a href=https://www.autocheck.com/vehiclehistory/vin-basics>VIN</a>')
    client = models.CharField('Client name', max_length=50,help_text="Name Surname")

    def __str__(self):
        return f'{self.client}, {self.car_model_ID}, {self.national_id}'

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'

class Order(models.Model):
    order_date = models.DateField('Date', default=datetime.today)
    car_id =models.ForeignKey('Car', on_delete=models.SET_NULL, null=True)
    deadline = models.DateField("Deadline", null=True)

    ORDER_STATUS = (
        ('Pending', 'Order Pending'),
        ('Accepted', 'Order Accepted'),
        ('In-progress', 'Service In-progress'),
        ('Done', 'Service Done'),
        ('Finalized', 'Order Finalized'),
    )

    status = models.CharField(
        max_length=11,
        choices=ORDER_STATUS,
        default='Pending',
        help_text='Order Status'
    )

    class Meta:
        ordering = ['order_date']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.car_id}, order date: {self.order_date}, deadline: {self.deadline}'


class OrderLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Order unique ID')
    service_id = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True, help_text="Add services to the order")
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.IntegerField('Quantity')

    def __str__(self):
        return f'Order ID: {self.id}, quantity - {self.quantity}'

    class Meta:
        verbose_name = 'Order line'
        verbose_name_plural = 'Order lines'