# from django.urls import path
# from . import views
#
# app_name = 'About_Us'
#
# urlpatterns = [
#     path('', views.about_us, name='aboutus'),
#     path('contact-us/', views.contact_us, name='contactus'),
#     # path('', views.About_us.as_view(), name='aboutus'),
#     # path('categories/', views.category_list_view, name='category_list'),
#     # path('categories/<int:pk>/', views.category_product_view, name='category_products'),
#     # path('categories/', views.Categories.as_view(), name='category_list'),
#     # path('category-wise-products/<pk>', views.CategoryWiseProducts.as_view(), name='category_wise_product_list'),
#     # path('category-wise-products/', views.CategoryWiseProducts.as_view(), name='category_wise_product_list'),
#     # path('offers/', views.Offers.as_view(), name='offers'),
#     # path('offer-details/', views.OfferDetails.as_view(), name='offer_details'),
#     # path('product/<pk>', views.ProductDetail.as_view(), name='product_detail'),
#     # path('search/', views.search_products, name='search_products'),
#     # path('product-suggestions/', views.product_suggestions, name='product_suggestions'),
#     # path('products-from-search/', views.product_list, name='product_list'),
#     # path('products-from-using_seemore/', views.product_list, name='load_more_products'),
#
# ]



from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import Setup_pageViewSet,BannerViewSet


router = DefaultRouter()
router.register('setup_page', Setup_pageViewSet)
router.register('slider-banner', BannerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]