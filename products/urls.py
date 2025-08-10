from django.urls import path
from . import views

urlpatterns = [
    #User urls
    path("", views.home, name="home"),
    path("sign-up/", views.sign_up, name="sign-up"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("view-cart/", views.view_cart, name="view-cart"),
    path("remove-item/<int:id>", views.remove_item, name="remove-item"),
    path("checkout/", views.checkout, name="checkout"),
    path("delete-cart/", views.delete_cart, name="delete-cart"),
    path("payment/", views.payment, name="payment"),
    
    #Admin urls
    path("admin/create-admin/", views.create_admin, name="create-admin"),
    path("admin/add-product/", views.add_product, name="add-product"),
    path("admin/update-product/", views.update_product, name="update-product"),
    path("admin/pending-orders/", views.pending_orders, name="pending-orders"),
    path("admin/confirm-order/<str:orderId>", views.confirm_order, name="confirm-order" ),
    path("confirmed-orders/", views.confirmed_orders, name="confirmed-orders"),
]
