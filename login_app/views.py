# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from django.urls import reverse
#
# # authentication
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, logout, authenticate
#
# # forms and models
# from login_app.models import Profile
# from login_app.forms import ProfileForm, SignupForm
#
# #  for show messages
# from django.contrib import messages
#
#
# # Create your views here.
# def cbbb(request):
#     return render(request, 'base.html')
#
#
# def sign_up(request):
#     form = SignupForm()
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Account Created Successfully ")
#             return HttpResponseRedirect(reverse('Login_App:login'))
#     return render(request, 'login_app/signup.html', context={'form': form})
#
#
# # login view
# def login_user(request):
#     form = AuthenticationForm()
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('Shop_App:home'))
#     return render(request, 'login_app/login.html', context={'form': form})
#
#
# @login_required
# def logout_user(request):
#     logout(request)
#     messages.warning(request, "You are logged out")
#     return HttpResponseRedirect(reverse('Shop_App:home'))
#
#
# @login_required
# def user_profile(request):
#     profile = Profile.objects.get(user=request.user)
#
#     form = ProfileForm(instance=profile)
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "change Saved")
#         form = ProfileForm(instance=profile)
#     return render(request, 'login_app/changeprofile.html', context={'form': form})


from rest_framework import viewsets, generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, Profile
from .serializers import UserSerializer, ProfileSerializer, RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# class RegisterViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer
#     permission_classes = [permissions.AllowAny]  # ✅ Register এর জন্য auth লাগবে না


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    # parser_classes = [MultiPartParser, FormParser]  # ✅ must be enabled

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

# class ProfileViewSet(viewsets.ModelViewSet):
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         # শুধু current logged-in user এর profile দেবে
#         return Profile.objects.filter(user=self.request.user)
#
#     def perform_create(self, serializer):
#         # profile create করলে user সেট হবে automatically
#         serializer.save(user=self.request.user)
