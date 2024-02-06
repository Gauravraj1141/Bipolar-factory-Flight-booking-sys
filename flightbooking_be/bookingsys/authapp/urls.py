from django.urls import path
from authapp.apis.simple_user.views_user_login_signup import UserSignup, CustomTokenObtainForUser
from authapp.apis.admin_user.views_admin_login import AdminLoginGenerateToken
from authapp.apis.simple_user.views_fetch_uesr_profile import FetchUserProfile

urlpatterns = [
    path('signup/', UserSignup.as_view(), name="signup"),
    path('login/', CustomTokenObtainForUser.as_view(), name='login'),
    path('user_profile/', FetchUserProfile.as_view(), name='user_profile'),
    path('admin_login/', AdminLoginGenerateToken.as_view(), name='admin_login'),

]
