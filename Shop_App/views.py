from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
import json
from json.encoder import JSONEncoder
from .models import Product, Comment, ProductCategory
from .forms import ProductForm, CommentModelForm
from ast import literal_eval

def home_view(request, *args, **kwargs):
    #FOR DEBUG the homepage flushes the session
    request.session.flush()
    return render(request, "Shop_App/home.html", {})


def add_to_order_view(request, *args, **kwargs):
    if request.method == "POST" and request.is_ajax:
        #FOR DEBUG -- DELETE COMPLETE SESSION OR A PART OF IT
        #request.session.flush()
        #del request.session['products_ordered']
        json_data = json.dumps(json.loads(request.body.decode('utf-8'))) #decoding the JSON data
        json_data = literal_eval(json_data) #ast.literal_eval so that it works as a dictionary properly
        
        products_ordered = []
        if request.session.get("products_ordered"):
            products_ordered = request.session.get("products_ordered")
        # Checks if the product added is a new product in dict, if not then increases only the amount

        new_position = True
        if products_ordered is not None:
            for k in products_ordered:
                if(json_data["product_name"] == k["product_name"]):
                    k["amount"]+=json_data["amount"]
                    new_position = False
                    break
        if new_position:
            products_ordered.append(json_data)

        request.session["products_ordered"] = products_ordered #changing the session data       

    return JsonResponse({"success":"true"})


def del_from_order_view(request, *args, **kwargs):
    print("Calling delete function")
    if request.method == "POST" and request.is_ajax:
        print("Statement ok")
        #FOR DEBUG -- DELETE COMPLETE SESSION OR A PART OF IT
        #request.session.flush()
        #del request.session['products_ordered']
        json_data = json.dumps(json.loads(request.body.decode('utf-8'))) #decoding the JSON data
        json_data = literal_eval(json_data) #ast.literal_eval so that it works as a dictionary properly
        
        products_ordered = request.session.get("products_ordered")
        # Checks if the product added is a new product in dict, if not then increases only the amount

        if products_ordered is not None:
            print("Not none")
            for k in products_ordered:
                print("K")
                if(json_data["product_name"] == k["product_name"]):
                    print("Deletion")
                    products_ordered.remove(k)

        print(products_ordered)
        request.session["products_ordered"] = products_ordered #changing the session data       

    return JsonResponse({"success":"true"})



def order_product_list_view(request, *args, **kwargs):
    if request.session.get("products_ordered"):
        data = {"products_ordered" : request.session.get("products_ordered")}
        print(data)

        for x in data["products_ordered"]:    
            q = Product.objects.get(name__iexact = x["product_name"])
            x["price"] = x["amount"] * q.price
        
        #json_response = json.dumps(data)
        return JsonResponse(data)
    return JsonResponse({"Status":"No order data available"})


def products_menu_list_view(request, *args, **kwargs):
    qs_all_products = Product.objects.all()
    product_list = [x.serialize() for x in qs_all_products]

    qs_categories = ProductCategory.objects.all()
    categories = [{"category" : x.category_name} for x in qs_categories]

    data = {"response" : {"product_list": product_list, 
                        "categories": categories}}

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
    form = ProductForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        obj = form.save(commit = False)

        catname = form.cleaned_data['category']
        cats = [(ProductCategory.objects.get(category_name__iexact = x)) for x in catname]

        obj.save()

        obj.category.set(cats)
        
        form.save_m2m()

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