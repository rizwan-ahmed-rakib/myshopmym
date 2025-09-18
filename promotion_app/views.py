# from django.shortcuts import render
# from .models import VideoPromotion
#
#
# def video_slider(request):
#     videos = VideoPromotion.objects.all()
#     # return render(request, 'shop_app/home.html', {'videos': videos})
#     return render(request, 'shop_app/embedvideo.html', {'videos': videos})



from rest_framework import viewsets, permissions
from .models import VideoPromotion
from .serializers import VideoPromotionSerializer


class VideoPromotionViewSet(viewsets.ModelViewSet):
    queryset = VideoPromotion.objects.all().order_by('-created_at')
    serializer_class = VideoPromotionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Optional: search by title
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset
