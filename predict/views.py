from django.shortcuts import render
from django.http import HttpResponse
import joblib


model = joblib.load('predict/models/RF_model.pkl')

def index(request):
    return render(request, "index.html")

def prediction(request):
    if request.method == 'POST':
        print(request.POST.dict())
        link = request.POST.get('link')
    return render(request, "predict.html")