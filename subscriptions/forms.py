from django import forms
from .models import UserSubscription,SubscriptionPlan
from django.contrib.auth import get_user_model
from math import floor
from datetime import timedelta, date
from decimal import Decimal


USER_MODEL = get_user_model()
RESERVATION_PRICE_PER_NIGHT = Decimal(10.50)
VAT_TAX_RATE = Decimal(0.05).quantize(Decimal('0.01'))

class UserSubscriptionCreationForm(forms.ModelForm):
    
    price = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'readonly':True}))
    class Meta:
        model = UserSubscription
        fields = ['customer', 'subscription', 'duration', 'starting_date']
    

    def __init__(self, user, *args, **kwargs):
        sub_plan_id = kwargs.pop('sub_plan_id', None)
        self.user_id = user.id
        super(UserSubscriptionCreationForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = USER_MODEL.objects.filter(id=user.id)
        self.fields['customer'].initial = user
        self.fields['customer'].empty_label = None
        self.fields['customer'].widget = forms.HiddenInput()

        self.fields['subscription'] = forms.ModelChoiceField(queryset= SubscriptionPlan.objects.all().order_by('-price_per_night').all())
        if sub_plan_id and SubscriptionPlan.objects.filter(id=sub_plan_id).exists():
            try:
                plan = SubscriptionPlan.objects.get(id=sub_plan_id)
                self.initial = {
                    'subscription' : plan,
                    'price' : f' NGN\xa0{plan.price_per_night}',
                    'duration' : 1
                }
            except Exception:
                pass
        self.fields['starting_date'].widget = forms.DateInput(attrs={'type' : 'date'})
        self.fields["duration"].label = 'Duration (Days)'
    
    def clean_customer(self):
        customer = self.cleaned_data.get('customer')
        if customer.id != self.user_id:
            raise forms.ValidationError('foul play')
        return customer

    def clean_duration(self):
        duration = self.cleaned_data.get('duration') 
        if duration == 0 or (duration != floor(duration)):
            raise forms.ValidationError('Please duration must be a whole number and cannot be less than 1')
        return duration

    def clean_starting_date(self):
        start_date = self.cleaned_data.get('starting_date')
        present_date = date.today()

        limit = timedelta(days=7) + present_date

        if (start_date >= limit) or (present_date > start_date):
            raise forms.ValidationError('Date must be within a week from now')

        reservation_fee = Decimal(Decimal((start_date - present_date) / timedelta(days=1))  *  RESERVATION_PRICE_PER_NIGHT).quantize(Decimal('0.01'))
        self.cleaned_data['reservation_fee'] = reservation_fee
    
        return start_date

    def clean_price(self):
        price = self.cleaned_data.get('price')
        price = price.replace('NGN','').replace('\xa0','').replace(',','')
        price = Decimal(price)
        return price

    def clean(self):
        clean_data = self.cleaned_data
        sub_plan = clean_data.get('subscription')
        duration = clean_data.get('duration')
        price = clean_data.get('price')
        reservation_fee = clean_data.get('reservation_fee')

        if reservation_fee == None or sub_plan == None or duration == None or price == None:
            raise forms.ValidationError('Invalid form details')
            
        expected_price = sub_plan.price_per_night * duration

        if (expected_price != price):
            raise forms.ValidationError('Invalid form details')


        # if not (sub_plan and duration and price and reservation_fee):
        #     raise forms.ValidationError('Invalid form details')

        tax = Decimal(VAT_TAX_RATE * (expected_price + reservation_fee)).quantize(Decimal('0.01'))

        self.cleaned_data['tax'] = tax 
        self.cleaned_data['total_price'] = Decimal(tax + expected_price + reservation_fee).quantize(Decimal('0.01'))
        
        return self.cleaned_data
    
    def get_payment_details(self):
        cleaned_data = self.cleaned_data
        payment_details = { key: str(value) for key, value in cleaned_data.items() if isinstance(value, Decimal) }
        return payment_details