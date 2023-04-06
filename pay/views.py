from django.shortcuts import render
from django.http import HttpResponse
from .models import plan,features,Subscription , PayPal
import datetime
# Create your views here.


# detail of plan

def plans(request):
    plans = plan.objects.all()
    feature_obj = features.objects.all()
    context={
        "plans":plans,
        "features": feature_obj,
    }
    return render (request, 'pay/plans.html', context) 


def plan_details(request, id):
    feature=features.objects.get(id=id)
    plans = plan.objects.get(id=id)
    paypal_info = PayPal.objects.last()
    context={
        "plans":plans,
        "feature": feature,
        "paypal_info":paypal_info,
    }
 
    return render (request, 'pay/plan_details.html' , context) 

