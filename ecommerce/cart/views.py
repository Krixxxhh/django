from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shop.models import Product
from cart.models import Cart,Order,Account
from django.http import HttpResponse
# Create your views here.

@login_required
#for displaying cart
def cartview(request):
    u=request.user
    total=0
    c=Cart.objects.filter(user=u)
    #to find the total
    for i in c:
        total=total+i.quantity*i.product.price

    return render (request,'cart.html',{'c':c,'total':total})


#for adding a particular product cart table
@login_required
def addtocart(request,p):
    p=Product.objects.get(id=p)
    u=request.user          #full details of the user will be stored inside
    try:
        cart=Cart.objects.get(user=u,product=p)     #to check if there is anything under that
        if(p.stock>0):
            cart.quantity+=1    # if there is it will be added

            cart.save()
            p.stock-=1
            p.save()
    except:
        if(p.stock>0):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock-=1
            p.save()
    return cartview(request)

def cart_remove(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (cart.quantity > 1):
            cart.quantity -= 1

            cart.save()
            p.stock += 1
            p.save()

        else:
            cart.delete()
            p.stock+=1
            p.save()
    except:
       pass
    return cartview(request)


def trash(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.stock=+cart.quantity
        p.save()
    except:
        pass
    return cartview(request)


@login_required
def orderform(request):
    if(request.method=="POST"):

        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']

        u=request.user
        c=Cart.objects.filter(user=u)

        total=0
        for i in c:
            total=total+i.quantity*i.product.price
        try:
            ac=Account.objects.get(acctnum=n)
            if(ac.amount>=total):
                ac.amount=ac.amount-total
                ac.save()

                for i in c:
                    o=Order.objects.create(user=u,product=i.product,address=a,phone=p,no_of_items=i.quantity,order_status="paid")
                    o.save()

                c.delete()
                msg="Order Placed Successfully"
                return render(request,'orderdetail.html',{'message':msg})
            else:
                msg = "Insufficient Fund,You can't Place  Order"
                return render(request,'orderdetail.html', {'message': msg})


        except:
            pass


    return render(request,'orderform.html')

def orderdetail(request):
    return render(request,'orderdetail.html')


def orderview(request):
    u = request.user
    o = Order.objects.filter(user=u)
    return render(request,'orderview.html',{'order':o,'u':u.username})