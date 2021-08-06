from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


#---------------important
#by problems with migrations uncoment following lines
# from django.contrib import admin

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
#and comment all below

from .views import ( manage_products_view, 
add_product_view, 
home_view,
products_menu_view,
products_menu_list_view,
comments_view,
comments_list_view,
add_comment_view)

urlpatterns = [
    path('manage_products/', manage_products_view, name="manage_products"),
    path('products_menu/', products_menu_view, name="products_menu"),
    path('products_menu_list', products_menu_list_view, name="products_menu_list"),
    path('add_product/', add_product_view, name="add_product"),
    path('comments/', comments_view, name="comments"),
    path('comments_list/', comments_list_view, name="comments_list"),
    path('add_comment/', add_comment_view, name="add_comment"),
    path('', home_view, name="homepage"),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)