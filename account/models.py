from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


def return_path(instance, filename):
    file_name = filename.split('.')[0]
    ext = filename.split('.')[-1]
    datetim = datetime.now().strftime("%Y_%m_%d--%H:%M:%S")
    return f"profile_pic/{instance.id}/{file_name}-{datetim}.{ext}"


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to=return_path,default="defaults/profile_pic/default-profile-pic.png")
