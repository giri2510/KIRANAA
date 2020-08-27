from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.utils.timezone import now


class Customer(models.Model):
    cust_id = models.IntegerField(primary_key=True)
    cust_user = models.ForeignKey(User, on_delete=models.CASCADE)
    cust_name = models.CharField(max_length=300, default='')
    cust_email = models.CharField(max_length=300, default='')
    cust_phone = models.CharField(max_length=300, default='')
    cust_address = models.CharField(max_length=300, default='')
    cust_city = models.CharField(max_length=500, default="")
    cust_state = models.CharField(max_length=500, default="")
    zip_code = models.CharField(max_length=500, default="")
    date_created = models.DateTimeField(auto_now_add=now)

    def __str__(self):
        return (self.cust_id) + " " + self.cust_name


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=200, default="")
    phone = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name
