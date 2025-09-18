
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', include('login_app.urls')),
    path('api/aboutus/', include('aboutUs_app.urls')),
    path('api/shop-app/', include('shop_app.urls')),
    path('api/order-app/', include('order_app.urls')),
    path('api/payment-app/', include('payment_app.urls')),
    path('api/promotion-app/', include('promotion_app.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
