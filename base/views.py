from django.shortcuts import render
from account.models import CustomUser
from subscriptions.models import SubscriptionPlan,UserSubscription

def cover_page(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        context['user'] = user
    return render(request,'cover-page.html', context)

def home_page(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        no_of_active_plans = len(UserSubscription.objects.filter(customer=user,is_active=True))
        context['no_of_active_plans'] = no_of_active_plans
    plans = sorted(SubscriptionPlan.objects.all(),key= lambda plan: plan.price_per_night,reverse=True)
    context['plans'] = plans
    return render(request,'home.html',context)

