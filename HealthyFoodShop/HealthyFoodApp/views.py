from django.shortcuts import render
from .forms import *
from .models import Category
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    categories = Category.objects.all()
    content={"categories": categories}
    return render(request, 'index.html',content)

@login_required
def out_of_stock(request):
    products=Product.objects.filter(quantity=0, category__active=True).all()
    form=ProductForm()
    content={"form":form,"products":products}

    if(request.method=='POST'):
        form_product=ProductForm(request.POST,files=request.FILES)
        if form_product.is_valid():
            product=form_product.save(commit=False)
            product.user=request.user
            product.category=form_product.cleaned_data['category']
            product.image=form_product.cleaned_data['image']
            product.save()
        else:
            print(form_product.errors)
    return render(request, 'out_of_stock.html',content)
