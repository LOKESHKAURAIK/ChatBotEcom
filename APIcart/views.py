from django.shortcuts import render
import requests
import json


def Cart(request):
    data = requests.get("ec2-34-207-242-88.compute-1.amazonaws.com")
    data = data.json()
    print(data)
    return render(request, "cart.html", {'data' : data})
