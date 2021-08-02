from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import Product, Comment
from .forms import ProductForm, CommentModelForm

def home_view(request, *args, **kwargs):

    return render(request, "Shop_App/home.html", {})


def products_menu_list_view(request, *args, **kwargs):
    qs_all_products = Product.objects.all()
    product_list = [{"id": x.id, "name": x.name,
    "description": x.description, 
    "creation_date": x.creation_date,
    "price" : x.price, 
    "image" : x.image.url} for x in qs_all_products]
    data = {"response" : product_list}
    return JsonResponse(data)

def manage_products_view(request, *args, **kwargs):
    qs_all_products = Product.objects.all()
    context = {"all_products":qs_all_products}
    return render(request, "Shop_App/manage_products.html", context)

def products_menu_view(request, *args, **kwargs):
    qs_all_products = Product.objects.all()
    context = {"all_products":qs_all_products}
    return render(request, "Shop_App/products_menu.html", context)

def add_product_view(request, *args, **kwargs):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit = False)
        obj.save()
        form = ProductForm() #clean after update
    context = {"form": form}
    return render(request, "Shop_App/add_product.html", context)

def comments_view(request, *args, **kwargs):
    context={}
    return render(request, "Shop_App/comments.html", context)

def comments_list_view(request, *args, **kwargs):
    qs_all_comments = Comment.objects.all()
    com_list = [x.serialize() for x in qs_all_comments]
    data = {'response': com_list}
    return JsonResponse(data)

def add_comment_view(request, *args, **kwargs):
    form = CommentModelForm(request.POST or None)
    next_url = request.POST.get("next") or None
    print("Next url: ",next_url)
    if form.is_valid():
        obj = form.save(commit = False)
        obj.save()
        print("Comment added")
        if next_url != None:
            return redirect(next_url)
        form = CommentModelForm()
    else:
        print("Form invalid")
    context = {"form": form}
    return render(request, "Shop_App/add_comment.html", context)



    """
    def add_comment_view(request, *args, **kwargs):
    form = CommentModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit = False)
        obj.save()
        print("Comment added")
        form = CommentModelForm()
    else:
        print("Form invalid")
    context = {"form": form}
    return render(request, "Shop_App/add_comment.html", context)
    """