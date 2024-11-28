from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Labukas, seniukouu!!\nSkanios kavelės gražios dienelės")
