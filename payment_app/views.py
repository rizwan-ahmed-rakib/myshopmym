from decimal import Decimal

from django.contrib.auth import get_user_model
# from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
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


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created")

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     cart_items = Cart.objects.filter(user=user, purchased=False)
    #     if not cart_items.exists():
    #         raise ValidationError({"error": "Cart is empty"})
    #
    #     billing = BillingAddress.objects.filter(user=user).first()
    #     if not billing:
    #         raise ValidationError({"error": "No billing address found"})
    #
    #     order_type = self.request.data.get("order_type", "COD")
    #
    #     if order_type == "ONLINE":
    #         # ❌ এখানে Order save করব না
    #         total = sum([ci.get_total() for ci in cart_items])
    #         return {
    #             "message": "Proceed to online payment",
    #             "cart_total": total,
    #             "cart_item_ids": [ci.id for ci in cart_items],  # gateway এ পাঠানোর জন্য
    #         }
    #
    #     # ✅ COD হলে সাথে সাথে order create
    #     order = serializer.save(
    #         user=user,
    #         ordered=True,
    #         order_type=order_type,
    #         delivery_type=self.request.data.get("delivery_type", "HOME_DELIVERY"),
    #         receiver_name=billing.name,
    #         receiver_email=billing.email,
    #         receiver_phone_number=billing.phone,
    #         receiver_address=billing.address,
    #         receiver_city=billing.city,
    #         receiver_zip_code=billing.zipcode,
    #         receiver_country=billing.country,
    #     )
    #     order.orderitems.set(cart_items)
    #     cart_items.update(purchased=True)
    #     return order

    def perform_create(self, serializer):
        user = self.request.user
        cart_items = Cart.objects.filter(user=user, purchased=False)
        if not cart_items.exists():
            raise ValidationError({"error": "Cart is empty"})

        billing = BillingAddress.objects.filter(user=user).first()
        if not billing:
            raise ValidationError({"error": "No billing address found"})

        order_type = self.request.data.get("order_type", "COD")

        if order_type == "COD":
            # ✅ COD order confirm immediately
            order = serializer.save(
                user=user,
                ordered=True,
                order_type=order_type,
                delivery_type=self.request.data.get("delivery_type", "HOME_DELIVERY"),
                receiver_name=billing.name,
                receiver_email=billing.email,
                receiver_phone_number=billing.phone,
                receiver_address=billing.address,
                receiver_city=billing.city,
                receiver_zip_code=billing.zipcode,
                receiver_country=billing.country,
            )
            order.orderitems.set(cart_items)
            cart_items.update(purchased=True)
            return order
        else:
            # ✅ ONLINE → create pending order (ordered=False)
            order = serializer.save(
                user=user,
                ordered=False,
                order_type=order_type,
                delivery_type=self.request.data.get("delivery_type", "HOME_DELIVERY"),
                receiver_name=billing.name,
                receiver_email=billing.email,
                receiver_phone_number=billing.phone,
                receiver_address=billing.address,
                receiver_city=billing.city,
                receiver_zip_code=billing.zipcode,
                receiver_country=billing.country,
            )
            order.orderitems.set(cart_items)
            return order

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
        return Response({"payment_url": response_data['GatewayPageURL']})


@csrf_exempt
def complete_payment(request):
    data = request.POST if request.method == 'POST' else request.GET
    status = data.get("status")
    tran_id = data.get("tran_id")
    val_id = data.get("val_id")
    order_id = data.get("value_a")

    if not order_id:
        return JsonResponse({"error": "order_id missing from SSLCommerz callback"}, status=400)

    try:
        order = Order.objects.get(id=int(order_id))
    except (Order.DoesNotExist, ValueError):
        return JsonResponse({"error": f"Invalid or missing order_id: {order_id}"}, status=404)

    # FRONTEND_URL = "https://myshopmym.com"  # production
    FRONTEND_URL = "http://localhost:3000"  # dev

    if status == "VALID":
        order.paymentId = val_id
        order.orderId = tran_id
        order.ordered = True
        order.save()
        return redirect(f"{FRONTEND_URL}/order")
    elif status == "FAILED":
        return redirect(f"{FRONTEND_URL}/payment-failed")
    elif status == "CANCELLED":
        return redirect(f"{FRONTEND_URL}/payment-cancelled")

    return JsonResponse({"message": "Invalid request or status"}, status=400)
