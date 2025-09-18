# from django.urls import path
# from . import views
#
# app_name = 'Shop_App'
#
# urlpatterns = [
#     path('', views.Home.as_view(), name='home'),
#     # path('categories/', views.category_list_view, name='category_list'),
#     # path('categories/<int:pk>/', views.category_product_view, name='category_products'),
#     # path('category_tree/', views.category_tree, name='category_tree'),
#     # path('categories/', views.Categories.as_view(), name='category_list'),
#     path('category-wise-products/<pk>', views.CategoryWiseProducts.as_view(), name='category_wise_product_list'),
#     # path('category-wise-products/', views.CategoryWiseProducts.as_view(), name='category_wise_product_list'),
#     path('offers/', views.Offers.as_view(), name='offers'),
#     path('offer-details/', views.OfferDetails.as_view(), name='offer_details'),
#     path('product/<pk>', views.ProductDetail.as_view(), name='product_detail'),
#     path('search/', views.search_products, name='search_products'),
#     path('product-suggestions/', views.product_suggestions, name='product_suggestions'),
#     path('products-from-search/', views.product_list, name='product_list'),
#     path('products-from-using_seemore/', views.product_list, name='load_more_products'),
#
# ]



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]
