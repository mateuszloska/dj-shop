from django.forms import (ModelForm, MultipleChoiceField,
CheckboxSelectMultiple)
from .models import Product, Comment, ProductCategory

class ProductForm(ModelForm):

    possible_categories1 = [("value", "visible name")]
    
    qs_cats = ProductCategory.objects.all()

    possible_categories = [(x.category_name, x.category_name) for x in qs_cats]
    print(possible_categories)

    category = MultipleChoiceField(
        required=True,
        widget=CheckboxSelectMultiple,
        choices=possible_categories)

    class Meta:
        model = Product
        fields = ['name',
        'is_vege','description',
        'price',  
        'image',]



class CommentModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'nickname', 'content']