from django.shortcuts import render,redirect
from shop.models import Category,Product
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def allcategories(request):
    c=Category.objects.all()
    return render(request,'category.html',{'c':c})


#for displaying products under a particular category
def allproducts(request,p):
    c=Category.objects.get(id=p)    #retrieves a particular category
    p=Product.objects.filter(category=c)    #
    return render(request,'product.html',{'c':c,'p':p})

def showdetail(request,p):
    p=Product.objects.get(id=p)
    return render(request,'detail.html',{'p':p})

def register(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        e = request.POST['e']
        f = request.POST['f']
        l = request.POST['l']

        if (cp == p):
            user = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)
            user.save()
            return redirect('shop:allcat')
        else:
            return HttpResponse("passwords are not the same")

    return render(request, 'register.html')


def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:allcat')
        else:
            return HttpResponse("Invalid Credentials")
    return render(request,'login.html')



def user_logout(request):
    logout(request)
    return allcategories(request)