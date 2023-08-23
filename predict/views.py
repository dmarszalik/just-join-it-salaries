from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, "index.html")

def prediction(request):
    if request.method == 'POST':
        print(request.POST.dict())
        link = request.POST.get('link')
    return render(request, "predict.html")