from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Plan,Feature,Subscription , PayPal
from django.contrib.auth.models import User 
import datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# detail of plan

def plans(request):
    plans = Plan.objects.all()
    feature_obj = Feature.objects.all()
    context={
        "plans":plans,
        "features": feature_obj,
    }
    return render (request, 'pay/plans.html', context) 


def plan_details(request, id):
    feature=Feature.objects.get(id=id)
    plans = Plan.objects.get(id=id)
    paypal_info = PayPal.objects.last()
    context={
        "plans":plans,
        "feature": feature,
        "paypal_info":paypal_info,
    }
 
    return render (request, 'pay/plan_details.html' , context) 


@csrf_exempt
def create_subscription(request): 
    if request.method == 'POST':
        # Values 
        #user , plan, start-date 

        user = request.POST.get ('user') 
        plan = request.POST.get('plan') 

        start_date = request.POST.get('start-date') 

        selected_plan = Plan.objects.get(name=plan)
        
        user_object = User.objects.get(username=user)
        
        start_date = datetime.datetime.strptime(start_date, '%d-%m-%Y')

        if selected_plan.unlimited == True: 
            end_date_time = start_date + datetime.timedelta(days=int(100000))
        else:
            end_date_time = start_date + datetime.timedelta(days=int(selected_plan.validaity))


        Subscription.objects.create(user=user_object, start_date=start_date, plan=selected_plan, end_date_time=end_date_time, videos_per_months=selected_plan.videos_per_months)
        return redirect('/') 
        

    return render(request, 'pages/checking.html')