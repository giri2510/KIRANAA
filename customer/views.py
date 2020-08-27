import json
import logging
from datetime import timezone
from math import ceil
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,UserManager,AbstractUser,AnonymousUser,PermissionManager
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.timezone import now
from .models import Customer, Contact
from store.models import Product,Order,Orderupdate,Orderitem

def home(request):
    # user creation
    if request.method == 'POST':
        username = request.POST['custusername']
        firstname = request.POST['custfirstname']
        lastname = request.POST['custlastname']
        email = request.POST['custemail']
        password1 = request.POST['custpassword1']
        password2 = request.POST['custpassword2']
        # create user
        if password1 != password2:
            messages.error(request, 'Password  Not Matching Please Try Again')
            return redirect('home')


        else:
            if not User.objects.filter(username=username).exists():
                myuser = User.objects.create_user(username=username, email=email, password=password1)
                """my_group = Group.objects.get(name='customer')
                my_group.user_set.add(myuser)"""
                myuser.first_name = firstname

                myuser.last_name = lastname
                """PERMISSIONS=['']
                for permission in PERMISSIONS:
                    name = 'Can {} {}'.format(permission, model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)
"""
                #myuser.save()
                messages.success(request, "Your account has been created ")
                return redirect("home")
            else:
                messages.error(request, "Username already exist")
                return redirect("home")
    else:
        return redirect(request,"customer/error.html")

def custlogin(request):
    if request.method == 'POST':
        username = request.POST["custlogin"]
        password = request.POST["custpsw"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successed")
            return redirect("/customer/")
        else:
            messages.error(request, "Invalid Username and Password")
            return redirect("/customer/")
    return redirect(request,"customer/error.html")

@login_required
def custlogout(request):
    logout(request)
    messages.success(request, "Logout Successfully ")
    return redirect('/customer')

def index(request):
    allproducts = []
    prodcateg = Product.objects.values('prod_category', 'prod_id')
    cats = {item['prod_category'] for item in prodcateg}

    for cat in cats:
        prod = Product.objects.filter(prod_category=cat)

        n = len(prodcateg)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allproducts.append([prod, range(1, nslides), nslides])
    # params={'no_of_slides':nslides,'range':range(1,nslides),'product':products}
    # allprod=[[products,range(1,nslides),nslides],
    #       [products,range(1,nslides),n],[products,range(1,nslides),nslides],
    #      [products,range(1,nslides),n],[products,range(1,nslides),nslides],
    #     [products,range(1,nslides),n]]

    params = {'allproducts': allproducts}

    return render(request, "customer/products.html", params)

def loginerror(request):
    user=request.user
    if user.is_authenticated:
        return redirect(request,"customer/home")
    else:
        return redirect(request,"customer/error.html")

@login_required
def checkout(request):
    js = []
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        items_json = request.POST.get('itemsJson', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        js.append(items_json)
        for k in js:
            l = json.loads(k)
            g = 0

            for i in l:
                ad = i[2]
                af = l[i][0]
                item = get_object_or_404(Product, prod_id=ad)
                order_qs = Order.objects.filter(person=request.user)
                if order_qs.exists():
                    order = order_qs[0]
                    if order.items.filter(item=item).exists():
                        messages.error(request, "This item is already placed .")

                    else:
                        order_item, created = Orderitem.objects.get_or_create(item=item, cust_order=request.user, quantity=af)

                        order.items.add(order_item)
                        messages.info(request, "This item was added to your cart.")
                else:
                    order = Order.objects.create(name=name, email=email, person=request.user, phone=phone,
                                                 address=address,
                                                 city=city, state=state, zip_code=zip_code)
                    order_item, created = Orderitem.objects.get_or_create(item=item, cust_order=request.user,
                                                                          quantity=af)

                    order.items.add(order_item)
                    messages.info(request, "This item was added to your cart.")
            id = order.id
            thank = True
            #update = Orderupdate(order_id=order.order_id, update_desc="Order has been placed")
            #update.save()
            #print("update",update)

        '''id1=str(order.order_id)
            orders1=str(order.items_json)
            prid=Product.product_id

            email=order.email
            msg = EmailMessage()
            msg['Subject'] = 'Order has been placed. Order Id is :  '+id1
            msg['From'] = 'localkiranashop@gmail.com'
            #msg['To'] = email
            msg['To'] =email
            msg['Cc']='localkiranashop@gmail.com,yogesh.ahire3388@gmail.com'
            msg.set_content('Check the Attachment \n\n'+orders1)


            #sub=forms.checkout()
            #if request.method=='POST':
            #    sub=forms.checkout(request.POST)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465)as smtp:
                smtp.login('localkiranashop@gmail.com', 'Kirana123456')
                smtp.send_message(msg)
                #recepient=str(sub['Email'].value())'''

        return render(request, 'customer/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'customer/checkout.html')

@login_required
@permission_required('Can view update order')
def tracker(request):
    if request.method == 'POST':
        orderid = request.POST.get('orderid', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderid, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'customer/tracker.html')

def productview(request, myid):
    product = Product.objects.filter(prod_id=myid)
    return render(request, 'customer/productview.html', {'product': product[0]})

def search(request):
    return render(request, 'customer/search.html')

def kirana(request):
    allproducts = []
    prodcateg = Product.objects.values('ownerprod', 'prod_id')
    cats = {item['ownerprod'] for item in prodcateg}
    for cat in cats:
        prod = Product.objects.filter(ownerprod=cat)
        allproducts.append([prod, range(0, 7)])
    params = {'allproducts': allproducts}

    params = {'allproducts': allproducts}

    return render(request,'customer/kirana.html',params)

def contact(request):
    return render(request, 'customer/contact.html')

def userlogout(request):
    logout(request)
    messages.success(request, "Logout Successfully ")
    return redirect('home')
