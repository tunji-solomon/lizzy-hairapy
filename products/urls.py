from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add-product/", views.add_product, name="add-product"),
    path("sign-up/", views.sign_up, name="sign-up"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("update-product/", views.update_product, name="update-product"),
    path("create-admin/", views.create_admin, name="create-admin"),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("view-cart/", views.view_cart, name="view-cart"),
]
