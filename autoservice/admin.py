from django.contrib import admin
from .models import Service, CarModel, Car, Order, OrderLine, OrderReview, Profile


class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'car_id','status', 'user', 'order_date', 'deadline')
    inlines = [OrderLineInLine]

    fieldsets = (
        (None, {
            'fields': ('car_id',)
        }),
        ('Availability', {
            'fields': ('status', 'deadline', 'user')
        }),
    )
class CarAdmin(admin.ModelAdmin):
    list_display = ('client', 'car_model_ID', 'national_id', 'VIN_code')
    list_filter = ('client', 'car_model_ID')
    search_fields = ('national_id', 'VIN_code')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'date_created', 'reviewer', 'content')

admin.site.register(Service, ServiceAdmin)
admin.site.register(CarModel)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
admin.site.register(OrderReview, OrderReviewAdmin)
admin.site.register(Profile)

