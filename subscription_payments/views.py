from django.shortcuts import render,reverse,redirect
from django.http import JsonResponse
from random import random,choices
from string import ascii_letters,digits
from subscriptions.models import SubscriptionPlan
from subscriptions.forms import UserSubscriptionCreationForm
from json import loads,dumps
from django.core.serializers import serialize,deserialize
from .models import Payment
import requests
from django.views.decorators.csrf import csrf_exempt

PAYMENT_GATEWAY_URL = 'http://127.0.0.1:9000'
API_KEY = 'Fe6KFxOCuSfW6u1LNNO5Lh9IQlev0P'
chars = ascii_letters + digits
plans = SubscriptionPlan.objects.all()


def id_generator(number= 8):
    return "".join(choices(chars, k=number))

def get_plan_prices(request):
    if request.method == 'GET':
        return JsonResponse({'error':'Bad Request'})

    data = {}
    for i in plans:
        data[str(i.id)] = i.price_per_night
    return JsonResponse(data)

def sub_plan_payment_page(request, plan_id=1):
    if not request.user.is_authenticated:
        return redirect('/')
    
    user = request.user
    context = {}
    context['plans'] = plans
    context['plan_id'] = plan_id
    form = UserSubscriptionCreationForm(user,sub_plan_id=plan_id)

    if request.method == 'POST':
        form = UserSubscriptionCreationForm(user=user,data=request.POST,sub_plan_id=plan_id)
        if form.is_valid():
            print('Thank You Jesus')

            payment_amt_data = form.get_payment_details()
            model = form.save(commit=False)
            serialized_model = serialize('jsonl', [model])
            request.session['model_instance'] = serialized_model
            request.session['payment_amt_data'] = payment_amt_data
            return redirect(reverse(payment_confirmation_page))
            
        else:
            print(form.errors)
    context["form"] = form
    return render(request,'payment/plan-payment.html',context)
    
    
def payment_confirmation_page(request):
    if not request.user.is_authenticated:
        return redirect('/')
    user = request.user
    client_id = id_generator()
    client_id += str(user.id)
    context = {}

    model_instance = request.session.get('model_instance', None)
    payment_amt_data = request.session.get('payment_amt_data', None)

    if model_instance == None or payment_amt_data == None:
        return redirect('/')

    des_obj = None
    for deserialized_obj in deserialize('jsonl', model_instance):
        des_obj = deserialized_obj.object
    context['obj'] = des_obj
    context['pmt_data'] = payment_amt_data

    if request.method == 'POST':
        print(reverse(payment_result_page),'lp')
        if request.headers.get('perms') == 'transaction-processing':
            body = loads(request.body)
            if body.get('permission') == 'yes':
                callback_code = id_generator()
                payment_model = Payment.objects.create(user=des_obj.customer,plan=des_obj.subscription,client_id=client_id,amount=payment_amt_data.get('total_price'),model_paid_for=model_instance,callback_code=callback_code)
                
                payload = {
                    'merchant-id' : f'{API_KEY}',
                    'client-id' : f'{client_id}',
                    'transaction-id' : f'{str(payment_model.id)}',
                    'amount' : f'{str(payment_model.amount)}',
                    'currency' : 'NGN',
                    'callback-url' : f'http://127.0.0.1:8000{reverse(payment_result_page)}',
                    'callback-code' : f'{str(payment_model.callback_code)}'
                }
                
                post_res = requests.post(url=f'{PAYMENT_GATEWAY_URL}/payment_api/payment-gateway/', data=dumps(payload), headers={'type-of-request' : 'transaction-details'})
                if post_res.status_code >= 400:
                    return render(request,'payment/error.html')

                print(post_res.json())
                return JsonResponse({'new_url' : f'{PAYMENT_GATEWAY_URL}/payment_api/payment-gateway/?client-id={client_id}&merchant-id={API_KEY}&transaction-id={payment_model.id}'})
            else:
                request.session.pop('model_instance', None)
                request.session.pop('payment_amt_data', None)
                return JsonResponse({'new_url' : f'/'})


            #return redirect(f'{PAYMENT_GATEWAY_URL}/payment_api/payment-gateway/?client-id={client_id}')
    return render(request, 'payment/payment-confirmation.html', context)


'''

{
    'status' : 'success',
    'callback-code' : 'itvfmfkd',
    'client-id' : 'dfgidojoi1'
    'api-key' : '',
}
'''
@csrf_exempt
def payment_result_page(request):
    if request.method != 'POST':
        return JsonResponse({'error' : 'Bad request'},status=400)
    
    try:
        data = loads(request.body)
    except Exception:
        return JsonResponse({'error' : 'Body is not valid json'}, status=400)

    status = data.get('status', None)
    callback_code = data.get('callback-code', None)
    client_id = data.get('client-id', None)
    transaction_id = data.get('transaction-id', None)
    api_key = data.get('api-key', None)
    
    if (not status) or (not callback_code) or (not client_id) or (not api_key) or (not transaction_id):
        return JsonResponse({'error' : 'Bad request'}, status=400)

    if status != 'success':
        return JsonResponse({'error' : 'Bad request'}, status=400)

    if Payment.objects.filter(client_id=client_id, callback_code=callback_code, id=transaction_id).exists():
        payment_obj = Payment.objects.get(client_id=client_id, callback_code=callback_code, id=transaction_id)
        if payment_obj.status == Payment.PENDING:
            payment_obj.status = Payment.SUCCESS

            deserialised_user_sub_model = deserialize('jsonl' ,payment_obj.model_paid_for)
            for model in deserialised_user_sub_model:
                user_sub_model = model.object
                user_sub_model.save()
                break  
            payment_obj.save()

    return JsonResponse({'sup': 'sup'})


    

    

