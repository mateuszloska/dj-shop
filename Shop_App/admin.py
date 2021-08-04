from django.contrib import admin
from .models import (Product, Comment,
ProductCategory, CategoryGroup)

admin.site.register(Comment)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(CategoryGroup)