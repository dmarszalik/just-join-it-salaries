from django.shortcuts import render
from django.http import HttpResponse
import joblib
from predict.offer import Offer


model = joblib.load('predict/models/RF_model_1.2.2.pkl')

job_offer_url = "https://justjoin.it/offers/bcf-software-sp-z-o-o-database-developer-postgresql-wroclaw"
offer_instance = Offer(job_offer_url)
offer_instance.preprocess()
processed_offer = offer_instance.get_processed_offer()
print(processed_offer)

pred = model.predict(processed_offer)

print(pred)

def index(request):
    return render(request, "index.html")

def prediction(request):
    if request.method == 'POST':
        print(request.POST.dict())
        link = request.POST.get('link')
    return render(request, "predict.html")