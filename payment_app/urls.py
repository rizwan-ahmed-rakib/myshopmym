# from django.urls import path
# from payment_app import views
#
# app_name = 'Payment_App'
# urlpatterns = [
#     path('checkout/', views.chekout, name="checkout"),
#     path('pay/', views.payment, name="payment"),
#     path('paymentStatus/', views.complete, name="complete"),
#     path('orders/', views.order_view, name="orders"),
#     path('purchase/<val_id>/<tran_id>', views.purchase, name="purchase"),
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urls import app_name

from .views import CartViewSet, OrderViewSet, BillingAddressViewSet, complete_payment

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'shipping-address', BillingAddressViewSet, basename='billing_address')


app_name = 'Payment_App'

urlpatterns = [
    path('', include(router.urls)),

    # ✅ Payment complete callback
    path('payment/complete/', complete_payment, name='complete'),
]
