from django.shortcuts import render
from django.http import HttpResponse


def home_view(request):
    print(request.GET)
    print(request.POST)
    return render(request, 'index.html')

# def output():
#     inputs = request.POST.get('input')