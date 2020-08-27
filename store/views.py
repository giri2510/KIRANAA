from math import ceil
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, UserManager, AbstractUser, AnonymousUser, PermissionManager
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

from .models import Merchentdb, Product, Orderitem, Finalorder, Order


def index(request):
    return render(request, 'store/home.html')


def userregister(request):
    if not Merchentdb.objects.filter(merch_name=request.user).exists():
        if request.method == 'POST':
            name = request.user
            reggno = request.POST.get('regno', '')
            shopname = request.POST.get('shopname', '')
            address1 = request.POST.get('address1', '') + " " + request.POST.get('landmark', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip', '')
            phone = request.POST.get('phone', '')
            commit = Merchentdb(merch_reggno=reggno, merch_name=name, merch_shop=shopname, merch_address=address1,
                                merch_phone=phone, merch_city=city, merch_state=state, merch_zip=zip_code, )
            commit.save()
            messages.success(request, "Details Added")
            return redirect("home")
    else:
        messages.error(request, "Data already exist")
        return redirect("home")
    return render(request, "store/index.html")


def usersignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # create user
        if password1 != password2:
            messages.error(request, 'Password  Not Matching Please Try Again')
            return redirect('home')


        else:
            if not User.objects.filter(username=username).exists():
                myuser = User.objects.create_user(username=username, email=email, password=password1, is_staff=True)
                myuser.first_name = firstname
                myuser.last_name = lastname
                # myuser.user_permissions.set(['sotre.add_product','sotre.view_product','store.delete_product','store.change_product'])
                permission1 = Permission.objects.get(name='Can add product')
                permission2 = Permission.objects.get(name='Can view product')
                permission3 = Permission.objects.get(name='Can change product')
                permission4 = Permission.objects.get(name='Can delete product')
                print(permission1)
                print(permission2)
                print(permission3)
                print(permission4)
                myuser.user_permissions.add(permission1)
                myuser.user_permissions.add(permission2)
                myuser.user_permissions.add(permission3)
                myuser.user_permissions.add(permission4)
                myuser.save()
                messages.success(request, "Your account has been created ")
                return redirect("home")
            else:
                messages.error(request, "Username already exist")
                return redirect("home")
    else:
        return HttpResponse('404 Not Found please try again')


def userlogin(request):
    if request.method == 'POST':
        username = request.POST["loginusername"]
        password = request.POST["psw"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login Successed")
            return redirect("home")
        else:
            messages.error(request, "Invalid Username and Password")
            return redirect("home")
    return HttpResponse("Please login")


@login_required
@permission_required('store.add_product', login_url='/store/')
def addproduct(request):
    if request.method == 'POST':
        prodname = request.POST.get('prodname', '')
        category = request.POST.get('category', '')
        subcategory = request.POST.get('subcategory', '')
        price = request.POST.get('price', '')
        desc = request.POST.get('desc', '')
        images = request.FILES['image']
        date = request.POST.get('updatedate', '')
        prod = Product(prod_name=prodname, owner=request.user,
                       ownerprod=Merchentdb.objects.get(merch_name=request.user),
                       prod_category=category, prod_subcategory=subcategory,
                       prod_desc=desc, prod_price=price, image=images, date=date)
        prod.save()
        messages.success(request, "Product Added Successfully")
        return render(request, 'store/addproduct.html')
    return render(request, 'store/addproduct.html')


@login_required
@permission_required('store.view_product', login_url='/store/')
def productview(request):
    allprod = []
    prodcateg = Product.objects.values('prod_category', 'prod_id')
    cats = {item['prod_category'] for item in prodcateg}
    for cat in cats:
        prod = Product.objects.filter(prod_category=cat, owner=request.user)
        allprod.append([prod, range(0, 7)])
    params = {'allprod': allprod}
    return render(request, 'store/productviews.html', params)


@login_required
@permission_required('store.change_product', login_url='/store/')
def produpdate(request, myid):
    product = Product.objects.filter(prod_id=myid)
    if request.method == 'POST':
        prodname = request.POST.get('updateprodname', '')
        category = request.POST.get('updatecategory', '')
        subcategory = request.POST.get('updatesubcategory', '')
        price = request.POST.get('updateprice', '')
        desc = request.POST.get('updatedesc', '')
        date = request.POST.get('uppdate', '')
        Product.objects.filter(prod_id=myid).update(prod_name=prodname,
                                                    prod_category=category, prod_subcategory=subcategory,
                                                    prod_desc=desc, prod_price=price, date=date)
        if request.method == 'POST' and request.FILES:
            m = Product.objects.get(prod_id=myid)
            images = request.FILES['updateimage']
            m.image = images
            m.save()
            messages.success(request, "Product has been updated successfully")
            return redirect('productviews')
        messages.success(request, "Product has been updated successfully")
        return redirect('productviews')
    return render(request, 'store/produpdate.html', {'product': product[0]})


@login_required
@permission_required('store.delete_product', login_url='/store/')
def prodelete(request, myid):
    product = Product.objects.get(prod_id=myid)
    messages.success(request, 'Product has been removed form DATABASE')
    product.delete()
    return redirect('productviews')


@login_required
def userlogout(request):
    logout(request)
    messages.success(request, "Logout Successfully ")
    return redirect('home')


@login_required
def orders(request):
    allown=[]
    asd=Order.objects.filter(items__item__owner=request.user).distinct()
    allown.append(asd)
    params={'allown':allown}
    return render(request, 'store/orders.html',params)  # , {'ac':asda})


def post_by_tag(request, myid):
    itmpr=[]
    cust = Order.objects.get(pk=myid)
    mulitems = Orderitem.objects.filter(cust_order_id=cust.person_id)
    for i in mulitems:
        if request.user==i.item.owner:

            if i.item.discount_price:
                rsqty=i.item.discount_price*i.quantity
                print("discount",rsqty)
                itmpr.append(rsqty)

            else:
                nonrsty=i.item.prod_price*i.quantity
                print("non disc",nonrsty)
                itmpr.append(nonrsty)
    print("itmpr",itmpr)
    total=0
    for j in itmpr:
        total=total+j
    context = {
        'cust': cust,
        'mulitems': mulitems,
        'total':total
    }
    return render(request, 'store/post_by_tag.html', context)
