from django.urls import path, include, re_path
from rest_framework import routers
from .views import BlogViewSet, LoginView, UserViewSet, RegisterView
from knox import views as knox_views

router = routers.DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blogs')
# router.register(r'register', UserViewSet, basename='register')

urlpatterns = [
    re_path(r'login', LoginView.as_view(), name='knox_login'),
    re_path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    re_path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    re_path(r'register/', RegisterView.as_view(), name='register')
]

urlpatterns += router.urls