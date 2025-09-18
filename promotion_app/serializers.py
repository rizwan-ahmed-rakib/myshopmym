from rest_framework import serializers
from .models import VideoPromotion


class VideoPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPromotion
        fields = [
            'id',
            'title',
            'full_video_url',
            'youtube_video_id',
            'facebook_video_id',
            'google_drive_video_id',
            'created_at'
        ]
        read_only_fields = ['youtube_video_id', 'facebook_video_id', 'google_drive_video_id', 'created_at']
