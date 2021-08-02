from django.forms import ModelForm
from .models import Product, Comment

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','description',
        'price', 'image']

class CommentModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'nickname', 'content']