from django.shortcuts import render
from django.http.response import HttpResponse
from apps.election.models import City, Country

# Create your views here.
def index(request):
    country = Country.objects.filter(deleted=0).all()
    context = {
        "country" :country
    }
    return render(request, "select.html", context)
# def product_detail(request,category_slug,product_id):
#     product=Product.objects.get(category__slug=category_slug,id=product_id)
#     products=Product.objects.all().order_by('-date')
#     context={
#         'product':product,
#         'products':products[0:5],
#     }
#     return render(request,'product.html',context)