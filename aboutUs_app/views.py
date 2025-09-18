# from django.shortcuts import render
# from django.views.generic import ListView
#
#
# class About_us(ListView):
#     # model = Product
#     template_name = 'aboutus/aboutus.html'
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     # context['categories'] = Category.objects.all()  # Category মডেলের সব অবজেক্ট পাঠানো হলো
#     #     # context['vid'] = VideoPromotion.objects.all()  # Category মডেলের সব অবজেক্ট পাঠানো হলো
#     #     return context
#
# def about_us(request):
#     return  render(request,'aboutus/aboutus.html')
#
# def contact_us(request):
#     return  render(request,'aboutus/cntactUs.html')



from rest_framework import viewsets
from .models import Setup_page,SliderBanners
from .serializers import Setup_page_Serializer,BannerSerializer


class Setup_pageViewSet(viewsets.ModelViewSet):
    queryset = Setup_page.objects.all()
    serializer_class = Setup_page_Serializer

class BannerViewSet(viewsets.ModelViewSet):
    queryset = SliderBanners.objects.all()
    serializer_class = BannerSerializer