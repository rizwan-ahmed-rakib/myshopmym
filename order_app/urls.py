# from django.urls import path
# from order_app import views
#
# app_name = 'Order_App'
#
# urlpatterns = [
#     path('add/<pk>/', views.add_to_cart, name="add"),
#     path('cart/', views.cart_view, name="cart"),
#     path('pre-order/', views.Preorder.as_view(), name="preorder"),
#     path('remove/<pk>/', views.remove_from_cart, name="remove"),
#     path('increase/<pk>/', views.increase_cart, name="increase"),
#     path('decrease/<pk>/', views.decrease_cart, name="decrease"),
# ]




from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, OrderViewSet


# app_name = 'Order_App'

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]
