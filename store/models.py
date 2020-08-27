from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.db import models
from django.utils import timezone
from django.utils.timezone import now


# Create your models here.


class Merchentdb(models.Model):
    merch_id = models.IntegerField(primary_key=True)
    merch_reggno = models.CharField(max_length=500, default='')
    merch_name = models.ForeignKey(User, on_delete=models.CASCADE)
    merch_shop = models.CharField(max_length=500, default='')
    merch_address = models.CharField(max_length=500, default='')
    merch_phone = models.CharField(max_length=500, default='')
    merch_city = models.CharField(max_length=500, default='')
    merch_state = models.CharField(max_length=500, default='')
    merch_zip = models.CharField(max_length=500, default='')
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.merch_shop


class Product(models.Model):
    prod_id = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ownerprod = models.ForeignKey(Merchentdb, on_delete=models.CASCADE, null=True)
    prod_category = models.CharField(max_length=500, default='')
    prod_subcategory = models.CharField(max_length=500, default='')
    prod_name = models.CharField(max_length=500, default='', unique=True)
    prod_desc = models.CharField(max_length=5000, default='')
    prod_price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='IMAGES/', editable=True)
    date = models.DateField(editable=True, default=now)

    def __str__(self):
        return self.prod_name


class Orderitem(models.Model):
    cust_order = models.ForeignKey(User, on_delete=models.CASCADE)
    # name= models.CharField(max_length=500,default='')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, to_field="prod_id")
    quantity = models.IntegerField(default='')

    # address=models.CharField(max_length=5000,default='')

    def __str__(self):
        return f"{self.quantity} of {self.item.prod_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.prod_price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    """def get_final_price(self):
        return self.get_total_item_price()"""

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Orderitem, through='Finalorder')
    name = models.CharField(max_length=500, default="")
    email = models.CharField(max_length=500, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=500, default="")
    state = models.CharField(max_length=500, default="")
    zip_code = models.CharField(max_length=500, default="")
    phone = models.CharField(max_length=500, default="")
    date_created = models.DateTimeField(auto_now_add=now)

    def __str__(self):
        return f"{self.person}"



    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total = order_item.get_final_price() + total
        return total


class Finalorder(models.Model):
    orderitems = models.ForeignKey(Orderitem, on_delete=models.CASCADE)
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)
    date_created = models.DateField(default=now)

    def __str__(self):
        return f"Order Id= {self.orders}"

    class Meta:
        unique_together = [['orderitems', 'orders']]


class Orderupdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="", null=True)
    custorders = models.ForeignKey(Order, on_delete=models.CASCADE)
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(timezone.now())

    def __str__(self):
        return self.update_desc[0:10] + "..."
