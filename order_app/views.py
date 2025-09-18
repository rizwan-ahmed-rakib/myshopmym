# from django.shortcuts import render, get_object_or_404, redirect
# # authentication
# from django.contrib.auth.decorators import login_required
# from django.views.generic import ListView
#
# # Model
# from order_app.models import Cart, Order
# from shop_app.models import Product
# # messages
# from django.contrib import messages
#
#
# # Create your views here.
# # @login_required
# def add_to_cart(request, pk):
#     item = get_object_or_404(Product, pk=pk)
#     order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         if order.orderitems.filter(item=item).exists():
#             order_item[0].quantity += 1
#             order_item[0].save()
#             messages.info(request, "this item quantity was updated")
#             return redirect("Shop_App:home")
#         else:
#             order.orderitems.add(order_item[0])
#             messages.info(request, "This item was added to your cart")
#             return redirect("Shop_App:home")
#     else:
#         order = Order(user=request.user)
#         order.save()
#         order.orderitems.add(order_item[0])
#         messages.info(request, "This item was added to your cart.")
#         return redirect("Shop_App:home")
#
#
# @login_required()
# def cart_view(request):
#     carts = Cart.objects.filter(user=request.user, purchased=False)
#     orders = Order.objects.filter(user=request.user, ordered=False)
#
#
#
#     if carts.exists() and orders.exists():
#         order = orders[0]
#         return render(request, 'order_app/cart.html', context={'carts': carts, 'order': order})
#     else:
#         messages.warning(request, "You don't have any item in your cart ")
#         # return redirect("Shop_App:home")
#         return render(request, 'order_app/emptycart.html')
#         # return render(request, 'order_app/cart.html')
#
#
# # for remove from cart
# @login_required()
# def remove_from_cart(request, pk):
#     item = get_object_or_404(Product, pk=pk)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         if order.orderitems.filter(item=item).exists():
#             order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
#             order.orderitems.remove(order_item)
#             order_item.delete()
#             messages.warning(request, "This item was removed from from your cart")
#             return redirect("Order_App:cart")
#         else:
#             messages.info(request, "This item was not in your cart.")
#             return redirect("Shop_App:home")
#
#     else:
#         messages.info(request, "you don't have an active order")
#         return redirect("Shop_App:home")
#
#
# # increase item in cart
# @login_required()
# def increase_cart(request, pk):
#     item = get_object_or_404(Product, pk=pk)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         if order.orderitems.filter(item=item).exists():
#             order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
#             if order_item.quantity >= 1:
#                 order_item.quantity += 1
#                 order_item.save()
#                 messages.warning(request, f"{item.name} quantity has been updated")
#                 return redirect("Order_App:cart")
#         else:
#             messages.info(request, f"{item.name} is not in your cart.")
#             return redirect("Shop_App:home")
#     else:
#         messages.info(request, "You don't have any active order")
#         return redirect("Shop_App:home")
#
#
# # decrease item in cart
# @login_required()
# def decrease_cart(request, pk):
#     item = get_object_or_404(Product, pk=pk)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         if order.orderitems.filter(item=item).exists():
#             order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
#             if order_item.quantity > 1:
#                 order_item.quantity -= 1
#                 order_item.save()
#                 messages.info(request, f"{item.name}quantity has been updated")
#                 return redirect("Order_App:cart")
#             else:
#                 order.orderitems.remove(order_item)
#                 order_item.delete()
#                 messages.warning(request, f"{item.name} item has been removed from your cart")
#                 return redirect('Order_App:cart')
#         else:
#             messages.info(request, f"{item.name} is not in your cart")
#             return redirect("Shop_App:home")
#     else:
#         messages.info(request, "You don't have any active order")
#         return redirect("Shop_App:home")
#
#
#
#
# class Preorder(ListView):
#     model = Product
#     template_name = 'order_app/preorder.html'
#     context_object_name = 'products'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # URL থেকে category_id নিচ্ছি
#         # category_id = self.kwargs.get('pk')
#         # category = get_object_or_404(Category, pk=category_id)
#
#         # প্রাসঙ্গিক ক্যাটাগরির প্রোডাক্ট ফিল্টার
#         # context['category'] = category
#         context['category'] = 'category'
#         # context['products'] = Product.objects.filter(category=category)
#         context['products'] =' Product.objects.filter(category=category)'
#
#         return context
#
#########################################################
##########################################


from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Cart, Order
from shop_app.models import Product
from .serializers import CartSerializer, OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend



class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,  # 🔍 Advanced filter support (filterset_fields)
        SearchFilter,         # 🔎 Search bar support (search_fields)
        OrderingFilter        # 📊 Optional ordering support
    ]
    filterset_fields = {
        "user":['exact'],
        "purchased":['exact'],
    }
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user, purchased=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # ✅ add to cart
    @action(detail=False, methods=['post'])
    def add(self, request):
        product_id = request.data.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user, item=product, purchased=False
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            return Response({"message": "Quantity updated"}, status=status.HTTP_200_OK)

        return Response({"message": "Item added to cart"}, status=status.HTTP_201_CREATED)

    # ✅ remove from cart
    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        cart_item = get_object_or_404(Cart, id=pk, user=request.user, purchased=False)
        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)

    # ✅ increase quantity
    @action(detail=True, methods=['post'])
    def increase(self, request, pk=None):
        cart_item = get_object_or_404(Cart, id=pk, user=request.user, purchased=False)
        cart_item.quantity += 1
        cart_item.save()
        return Response({"message": "Quantity increased"}, status=status.HTTP_200_OK)

    # ✅ decrease quantity
    @action(detail=True, methods=['post'])
    def decrease(self, request, pk=None):
        cart_item = get_object_or_404(Cart, id=pk, user=request.user, purchased=False)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return Response({"message": "Quantity decreased"}, status=status.HTTP_200_OK)
        else:
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Checkout এর মতো কাজ করবে
        user = self.request.user
        cart_items = Cart.objects.filter(user=user, purchased=False)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = serializer.save(user=user, ordered=True)
        order.orderitems.set(cart_items)
        cart_items.update(purchased=True)

        return order
