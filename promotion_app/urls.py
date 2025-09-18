# from django.urls import path
# from .views import video_slider
#
# urlpatterns = [
#     path('videos/', video_slider, name='video_slider'),
# ]



from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import VideoPromotionViewSet

router = DefaultRouter()
router.register(r'videos', VideoPromotionViewSet, basename='video')

urlpatterns = [
    path('', include(router.urls)),
]
