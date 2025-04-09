from django.db import models
from account.models import CustomUser
from datetime import date,timedelta,datetime
import random
from django.core.exceptions import ValidationError

def photo_path(instance, filename):
    file_name = filename.split('.')[0]
    ext = filename.split('.')[-1]
    date_time = datetime.now().strftime('%Y_%m_%d--%H:%M:%S')
    return f"subscription-photos/{instance.id}/{file_name}--{date_time}.{ext}"

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10000000,decimal_places=2)
    description = models.CharField(max_length=100000, null=True, blank=True)
    display_color = models.CharField(max_length=10,default='#FFFFFF')
    alt_display_color = models.CharField(max_length=10,default='#000000')
    photo = models.ImageField(upload_to= photo_path, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

class Room(models.Model):
    def model_default():
        return 1  # id of the default model
        
    room_number = models.CharField(max_length=6)
    room_class = models.ForeignKey(SubscriptionPlan, models.SET_DEFAULT, default=model_default)
    occupied = models.BooleanField(default=False)

    def is_occupied(self):
        return self.occupied

    def __str__(self):
        return self.room_number

class UserSubscription(models.Model):
    def room_default():
        return None
    customer = models.ForeignKey(CustomUser,models.CASCADE)
    subscription = models.ForeignKey(SubscriptionPlan,models.SET_NULL,null=True)
    subscriptionId = models.CharField(max_length=100000000000000, default=None)
    room = models.OneToOneField(Room, models.SET_NULL,default=None, null=True)
    duration = models.PositiveIntegerField(default=1)
    starting_date = models.DateField(default = datetime.now)
    expiry_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    red_alert = models.BooleanField(default=False)

    def check_if_active(self):
        return self.is_active
    
    def check_if_red(self):
        return self.red_alert

    def __str__(self):
        return f'{self.subscriptionId}'

    def save(self, *args, **kwargs):

        if self.subscriptionId == None:
            custom_id = ''.join([str(i) for i in random.choices(range(10),k=6)])
            self.subscriptionId = str(self.customer.id) + custom_id

        DEFINITE_LOG_OUT_TIME = 12                    #representing 12noon that day

        if not self.expiry_date:
            expiry_date = self.starting_date + timedelta(self.duration)
            day = expiry_date.day
            month = expiry_date.month
            year = expiry_date.year
            expiry_datetime = datetime(year=year,month=month,day=day)
            self.expiry_date = expiry_datetime + timedelta(hours=DEFINITE_LOG_OUT_TIME)

        if self.room == None:
            rooms = Room.objects.filter(occupied=False, room_class=self.subscription)
            if len(rooms) == 0:
                raise ValidationError('No rooms available')
            random_room = random.choice(rooms)
            random_room.occupied = True
            random_room.save()
            self.room = random_room
            
            
        return super(UserSubscription,self).save( *args, **kwargs)