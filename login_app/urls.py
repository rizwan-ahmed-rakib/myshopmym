# from django.urls import path
# from login_app import views
#
# app_name = 'Login_App'
#
# urlpatterns = [
#     path('signup/', views.sign_up, name='signup'),
#     path('login/', views.login_user, name='login'),
#     path('logout/', views.logout_user, name='logout'),
#     path('profile/', views.user_profile, name='profile'),
# ]



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet, RegisterView

# app_name = 'Login_App'


router = DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'profiles', ProfileViewSet, basename="profile")
router.register(r'profiles', ProfileViewSet)
# router.register(r'register', RegisterViewSet,basename="register"),

urlpatterns = [
    path('', include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),

]
