from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
# Create your views here.
def searchproducts(request):
    if(request.method=="POST"):
        p=None
        query=""
        query=request.POST['q']
        p=Product.objects.filter(Q(name__icontains=query) | Q(desc__icontains=query))

    return render(request,'search.html',{'p':p,'q':query})