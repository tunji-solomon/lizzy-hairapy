from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add-product", views.add_product, name="add-product")
]
