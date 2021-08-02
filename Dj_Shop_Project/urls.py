from django.contrib import admin
from django.urls import path, include
from Shop_App import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Shop_App.urls")),
]
