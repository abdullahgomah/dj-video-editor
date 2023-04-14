from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from pay.models import * 
from .models import Contact
import datetime 

# Create your views here.
def index(request):
    check_plan(request) 
    context= {}
    return render(request, 'pages/index.html', context)


@login_required
def check_plan(request):

    user = request.user 
    try:
        subscription = Subscription.objects.get(user=user)
        if datetime.date.today() > subscription.end_date_time: 
            # print('Please Renew Your Subscription')
            # هنا يجب تجديد الاشتراك
            subscription.delete() 
        else:
            # هنا اشتراكك ما زال يعمل
            # print("Your Subscription Is Still Active")
            pass 
    except:
        pass 



def contact_form(request):

    if request.POST: 
        email = request.POST.get('email')
        details = request.POST.get('details') 
        plan = request.POST.get('plan') 

        new_contact = Contact.objects.create(email=email, details=details, plan=plan) 
        new_contact.save() 

        return render(request, 'pages/contact_completed.html') 

        

    plans = Plan.objects.all() 

    context = {
        'plans': plans,
    } 
    return render(request, 'pages/contact.html', context) 


def handler404(request, exception):
    return render(request, 'pages/404.html', status=404)

def handler500(request):
    return render(request, 'pages/500.html', status=500) 
