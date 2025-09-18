# from django.http import HttpResponseRedirect
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.urls import reverse
# # models and forms
# from order_app.models import Order, Cart
# from payment_app.models import BillingAddress
# from payment_app.forms import BillingForm
# #
# from django.contrib.auth.decorators import login_required
# # for payment
# import requests
#
# from django.conf import settings
# from sslcommerz_python.payment import SSLCSession
#
# from decimal import Decimal
#
# import socket
# from django.views.decorators.csrf import csrf_exempt
#
#
# # Create your views here.
#
# # @login_required
# # def chekout(request):
# #     saved_address = BillingAddress.objects.get_or_create(user=request.user)
# #     saved_address = saved_address[0]
# #     form = BillingForm(instance=saved_address)
# #     if request.method == "POST":
# #         form = BillingForm(request.POST, instance=saved_address)
# #         if form.is_valid():
# #             form.save()
# #             form = BillingForm(instance=saved_address)
# #             messages.success(request, f"Shipping Address Saved")
# #     order_qs = Order.objects.filter(user=request.user, ordered=False)
# #     order_items = order_qs[0].orderitems.all()
# #     order_total = order_qs[0].get_totals()        # get_totals()
# #     return render(request, 'payment_app/checkout.html',
# #                   context={"form": form, "order_items": order_items, "order_total": order_total,
# #                            "saved_address": saved_address})
#
#
#
#
# @login_required
# def chekout(request):
#     saved_address = BillingAddress.objects.get_or_create(user=request.user)
#     saved_address = saved_address[0]
#     form = BillingForm(instance=saved_address)
#     if request.method == "POST":
#         form = BillingForm(request.POST, instance=saved_address)
#         if form.is_valid():
#             form.save()
#             form = BillingForm(instance=saved_address)
#             messages.success(request, f"Shipping Address Saved")
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     # order_items = order_qs[0].orderitems.all()
#     # order_total = order_qs[0].get_totals()        # get_totals()
#     return render(request, 'payment_app/checkout.html',
#                   context={"form": '1', "order_items": '2', "order_total": '3',
#                            "saved_address": '4'})
#
#
#
# @login_required()
# def payment(request):
#     saved_address = BillingAddress.objects.get_or_create(user_id=request.user)
#     saved_address = saved_address[0]
#     if not saved_address.is_fully_filled():
#         messages.info(request, f"please complete shipping address")
#         return redirect("Payment_App:checkout")
#     if not request.user.profile.is_fully_filled():
#         messages.info(request, f"please complete profile details")
#         return redirect("Login_App:profile")
#     store_id = 'taqwa6471a2e1abae1'
#     API_Key = 'taqwa6471a2e1abae1@ssl'
#     mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
#                             sslc_store_pass=API_Key)
#
#     status_url = request.build_absolute_uri(reverse('Payment_App:complete'))
#
#     mypayment.set_urls(success_url=status_url, fail_url=status_url,
#                        cancel_url=status_url, ipn_url=status_url)
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     order_items = order_qs[0].orderitems.all()
#     order_items_count = order_qs[0].orderitems.count()
#     order_total = order_qs[0].get_totals()
#
#     mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed',
#                                       product_name=order_items, num_of_item=order_items_count,
#                                       shipping_method='Courier',
#                                       product_profile='None')
#     current_user = request.user
#     mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email,
#                                 address1=current_user.profile.address_1,
#                                 address2=current_user.profile.address_1, city=current_user.profile.city,
#                                 postcode=current_user.profile.zipcode, country=current_user.profile.country,
#                                 phone=current_user.profile.phone)
#
#     mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=saved_address.address,
#                                 city=saved_address.city, postcode=saved_address.zipcode,
#                                 country=saved_address.country)
#
#     response_data = mypayment.init_payment()
#     print(response_data)
#     return redirect(response_data['GatewayPageURL'])
#
#
# @csrf_exempt
# def complete(request):
#     if request.method == 'POST' or request.method == 'post':
#         payment_data = request.POST
#         status = payment_data['status']
#         if status == 'VALID':
#             val_id = payment_data['val_id']
#             tran_id = payment_data['tran_id']
#             messages.success(request, f"Your Payment Completed Successfully")
#             return HttpResponseRedirect(reverse('Payment_App:purchase',
#                                                 kwargs={'val_id': val_id, 'tran_id': tran_id}, ))
#         elif status == 'FAILED':
#             messages.warning(request, f"Your Payment Failed! Please Try Again ")
#
#     return render(request, 'payment_app/complete.html', context={})
#
#
# @login_required
# def purchase(request, val_id, tran_id):
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     order = order_qs[0]
#     orderId = tran_id
#     order.ordered = True
#     order.orderId = orderId
#     order.paymentId = val_id
#     order.save()
#     cart_items = Cart.objects.filter(user=request.user, purchased=False)
#     for item in cart_items:
#         item.purchased = True
#         item.save()
#     return HttpResponseRedirect(reverse('Shop_App:home'))
#
#
# @login_required
# def order_view(request):
#     try:
#         orders = Order.objects.filter(user=request.user, ordered=True)
#         context = {"orders": orders}
#     except:
#         messages.warning(request, "you do not have any active order")
#         return redirect("Shop_App:home")
#     return render(request, "payment_app/order.html",context)


#########################################################

# from decimal import Decimal
# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponseRedirect
#
# from sslcommerz_python.payment import SSLCSession
#
# from order_app.models import Order, Cart
# from payment_app.models import BillingAddress
# from payment_app.forms import BillingForm
#
# # ----------------------------
# # Checkout view
# # ----------------------------
# @login_required
# def checkout(request):
#     saved_address, created = BillingAddress.objects.get_or_create(user=request.user)
#     form = BillingForm(instance=saved_address)
#
#     if request.method == "POST":
#         form = BillingForm(request.POST, instance=saved_address)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Shipping Address Saved")
#
#     order = Order.objects.filter(user=request.user, ordered=False).first()
#     if not order:
#         messages.warning(request, "No active order found.")
#         return redirect("Shop_App:home")
#
#     order_items = order.orderitems.all()
#     order_total = order.get_totals()
#
#     context = {
#         "form": form,
#         "order_items": order_items,
#         "order_total": order_total,
#         "saved_address": saved_address
#     }
#     return render(request, 'payment_app/checkout.html', context)
#
#
# # ----------------------------
# # Payment initiation
# # ----------------------------
# @login_required
# def payment(request):
#     saved_address = BillingAddress.objects.filter(user=request.user).first()
#     if not saved_address or not saved_address.is_fully_filled():
#         messages.info(request, "Please complete shipping address")
#         return redirect("Payment_App:checkout")
#
#     if not request.user.profile.is_fully_filled():
#         messages.info(request, "Please complete profile details")
#         return redirect("Login_App:profile")
#
#     order = Order.objects.filter(user=request.user, ordered=False).first()
#     if not order:
#         messages.warning(request, "No active order found.")
#         return redirect("Shop_App:home")
#
#     order_items = order.orderitems.all()
#     order_items_count = order_items.count()
#     order_total = order.get_totals()
#
#     # Initialize SSLCommerz
#     store_id = 'taqwa6471a2e1abae1'
#     API_Key = 'taqwa6471a2e1abae1@ssl'
#     sslc = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_Key)
#
#     status_url = request.build_absolute_uri(reverse('Payment_App:complete'))
#     sslc.set_urls(success_url=status_url, fail_url=status_url,
#                   cancel_url=status_url, ipn_url=status_url)
#
#     # Prepare product names as string
#     product_names = ", ".join([item.item.name for item in order_items])
#     sslc.set_product_integration(
#         total_amount=Decimal(order_total),
#         currency='BDT',
#         product_category='Mixed',
#         product_name=product_names,
#         num_of_item=order_items_count,
#         shipping_method='Courier',
#         product_profile='None'
#     )
#
#     # Customer info
#     profile = request.user.profile
#     sslc.set_customer_info(
#         name=profile.full_name,
#         email=request.user.email,
#         address1=profile.address_1,
#         address2=profile.address_1,
#         city=profile.city,
#         postcode=profile.zipcode,
#         country=profile.country,
#         phone=profile.phone
#     )
#
#     # Shipping info
#     sslc.set_shipping_info(
#         shipping_to=profile.full_name,
#         address=saved_address.address,
#         city=saved_address.city,
#         postcode=saved_address.zipcode,
#         country=saved_address.country
#     )
#
#     response_data = sslc.init_payment()
#     return redirect(response_data['GatewayPageURL'])
#
#
# # ----------------------------
# # Payment completion (SSLCommerz callback)
# # ----------------------------
# @csrf_exempt
# def complete(request):
#     if request.method.lower() == 'post':
#         payment_data = request.POST
#         status = payment_data.get('status')
#
#         if status == 'VALID':
#             val_id = payment_data.get('val_id')
#             tran_id = payment_data.get('tran_id')
#             messages.success(request, "Your Payment Completed Successfully")
#             return HttpResponseRedirect(reverse(
#                 'Payment_App:purchase',
#                 kwargs={'val_id': val_id, 'tran_id': tran_id}
#             ))
#
#         elif status == 'FAILED':
#             messages.warning(request, "Your Payment Failed! Please Try Again")
#
#     return render(request, 'payment_app/complete.html', context={})
#
#
# # ----------------------------
# # Mark order & cart items as purchased
# # ----------------------------
# @login_required
# def purchase(request, val_id, tran_id):
#     order = Order.objects.filter(user=request.user, ordered=False).first()
#     if not order:
#         messages.warning(request, "No active order found.")
#         return redirect("Shop_App:home")
#
#     order.ordered = True
#     order.paymentId = val_id
#     order.orderId = tran_id
#     order.save()
#
#     Cart.objects.filter(user=request.user, purchased=False).update(purchased=True)
#
#     messages.success(request, "Order completed successfully!")
#     return redirect("Shop_App:home")
#
#
# # ----------------------------
# # Order history view
# # ----------------------------
# @login_required
# def order_view(request):
#     orders = Order.objects.filter(user=request.user, ordered=True)
#     if not orders.exists():
#         messages.warning(request, "You do not have any completed orders.")
#         return redirect("Shop_App:home")
#
#     return render(request, "payment_app/order.html", context={"orders": orders})

##############################################


from decimal import Decimal

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from rest_framework.reverse import reverse

from order_app.serializers import CartSerializer, OrderSerializer
from sslcommerz_python.payment import SSLCSession

from order_app.models import Cart, Order
from shop_app.models import Product
from payment_app.models import BillingAddress
from payment_app.serializers import BillingAddressSerializer


# -----------------------------
# Cart API
# -----------------------------
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user, purchased=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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

        return Response({"message": "Item added"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        cart_item = get_object_or_404(Cart, id=pk, user=request.user, purchased=False)
        cart_item.delete()
        return Response({"message": "Item removed"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def increase(self, request, pk=None):
        cart_item = get_object_or_404(Cart, id=pk, user=request.user, purchased=False)
        cart_item.quantity += 1
        cart_item.save()
        return Response({"message": "Quantity increased"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def decrease(self, request, pk=None):
        cart_item = get_object_or_404(Cart, id=pk, user=request.user, purchased=False)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return Response({"message": "Quantity decreased"}, status=status.HTTP_200_OK)
        else:
            cart_item.delete()
            return Response({"message": "Item removed"}, status=status.HTTP_200_OK)


# -----------------------------
# Billing Address API
# -----------------------------
class BillingAddressViewSet(viewsets.ModelViewSet):
    serializer_class = BillingAddressSerializer

    def get_queryset(self):
        return BillingAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# -----------------------------
# Order / Checkout API
# -----------------------------
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Checkout: create order from cart
        user = self.request.user
        cart_items = Cart.objects.filter(user=user, purchased=False)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = serializer.save(user=user, ordered=True)
        order.orderitems.set(cart_items)
        cart_items.update(purchased=True)
        return order

    # -------------------------
    # Payment initiation endpoint
    # -------------------------
    @action(detail=True, methods=['get'])
    def initiate_payment(self, request, pk=None):
        order = get_object_or_404(Order, id=pk, user=request.user)
        billing = BillingAddress.objects.filter(user=request.user).first()
        profile = request.user.profile

        if not billing or not billing.is_fully_filled():
            return Response({"error": "Complete billing address"}, status=status.HTTP_400_BAD_REQUEST)
        if not profile.is_fully_filled():
            return Response({"error": "Complete profile details"}, status=status.HTTP_400_BAD_REQUEST)

        store_id = 'taqwa6471a2e1abae1'
        API_Key = 'taqwa6471a2e1abae1@ssl'
        sslc = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_Key)

        status_url = request.build_absolute_uri(reverse('Payment_App:complete'))
        sslc.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

        order_items = order.orderitems.all()
        product_names = ", ".join([item.item.name for item in order_items])
        sslc.set_product_integration(
            total_amount=Decimal(order.get_totals()),
            currency='BDT',
            product_category='Mixed',
            product_name=product_names,
            num_of_item=order_items.count(),
            shipping_method='Courier',
            product_profile='None',
            # value_a=order.id # ✅ order.id SSLCommerz-এ পাঠানো হলো

        )

        sslc.set_customer_info(
            name=profile.full_name,
            email=request.user.email,
            address1=profile.address_1,
            address2=profile.address_1,
            city=profile.city,
            postcode=profile.zipcode,
            country=profile.country,
            phone=profile.phone
        )

        sslc.set_shipping_info(
            shipping_to=profile.full_name,
            address=billing.address,
            city=billing.city,
            postcode=billing.zipcode,
            country=billing.country
        )

        sslc.set_additional_values(value_a=str(order.id))

        response_data = sslc.init_payment()
        # response_data['GatewayPageURL'] += f"&value_a={order.id}"
        return Response({"payment_url": response_data['GatewayPageURL']})


# @csrf_exempt  # SSLCommerz থেকে callback আসবে, তাই exempt করা হলো
# def complete_payment(request):
#     if request.method == 'POST' or request.method == 'GET':
#         data = request.POST if request.method == 'POST' else request.GET
#         status = data.get("status")
#
#         if status == "VALID":
#             tran_id = data.get("tran_id")
#             val_id = data.get("val_id")
#             order_id = data.get("value_a")  # তুমি চাইলে order.id এখানে পাঠাতে পারো
#
#             # Order খুঁজে বের করো
#             try:
#                 order = Order.objects.get(id=order_id)
#                 order.paymentId = val_id
#                 order.orderId = tran_id
#                 order.ordered = True
#                 order.save()
#             except Order.DoesNotExist:
#                 return JsonResponse({"error": "Order not found"}, status=404)
#
#             # ✅ Payment success → success page এ redirect
#             return redirect("/payment-success")
#
#         elif status == "FAILED":
#             return redirect("/payment-failed")
#
#         elif status == "CANCELLED":
#             return redirect("/payment-cancelled")
#
#     return JsonResponse({"message": "Invalid request"}, status=400)


@csrf_exempt
def complete_payment(request):
    # SSLCommerz callback data (GET বা POST)
    data = request.POST if request.method == 'POST' else request.GET
    print("✅ SSLCommerz Callback Data:", data)  # Debugging log

    status = data.get("status")
    tran_id = data.get("tran_id")
    val_id = data.get("val_id")
    order_id = data.get("value_a")  # আমরা init_payment এ পাঠিয়েছিলাম

    print("👉 status:", status)
    print("👉 tran_id:", tran_id)
    print("👉 val_id:", val_id)
    print("👉 order_id:", order_id)

    if not order_id:
        return JsonResponse({"error": "order_id missing from SSLCommerz callback"}, status=400)

    try:
        order = Order.objects.get(id=int(order_id))
    except (Order.DoesNotExist, ValueError):
        return JsonResponse({"error": f"Invalid or missing order_id: {order_id}"}, status=404)

    FRONTEND_URL = "http://localhost:3000"  # তোমার React dev server URL

    if status == "VALID":
        order.paymentId = val_id
        order.orderId = tran_id
        order.ordered = True
        order.save()
        print("✅ Payment Successful, Order updated:", order.id)
        # return redirect("/payment-success")
        return redirect(f"{FRONTEND_URL}/order")


    elif status == "FAILED":
        print("❌ Payment Failed for order:", order.id)
        return redirect("/payment-failed")

    elif status == "CANCELLED":
        print("⚠️ Payment Cancelled for order:", order.id)
        return redirect("/payment-cancelled")

    return JsonResponse({"message": "Invalid request or status"}, status=400)
