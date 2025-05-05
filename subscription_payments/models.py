from django.db import models
from django.contrib.auth import get_user_model
from subscriptions.models import SubscriptionPlan


USER_MODEL = get_user_model()

class Payment(models.Model):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failure'

    STATUS = [

        (PENDING, 'pending'),
        (SUCCESS, 'success'),
        (FAILED, 'failure'),
    ]
    
    user = models.ForeignKey(USER_MODEL,on_delete=models.SET_NULL,null=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    client_id = models.CharField(max_length=30,default='none')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS, default=PENDING)
    model_paid_for = models.JSONField(default=dict)
    callback_code = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)