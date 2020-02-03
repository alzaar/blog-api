from blog.serializers import BlogSerializer, UserSerializer, LoginSerializer, RegisterSerializer
from .models import Blog
# from rest_framework.views import APIView
from rest_framework import response
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework import generics
class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]
    

    def create(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        request.data['created_by'] = user.id
        return super().create(request, *args, **kwargs)

    def list(self, request):
        blogs = Blog.objects.filter(created_by=request.user.id)
        data = BlogSerializer(blogs, many=True).data
        return response.Response({'data': data, 'user': request.user.username,  'id': request.user.id})

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def destroy(self, request, pk=None):
        user = User.objects.get(username=request.user)
        return super().destroy(self, request, pk=user.id)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return response.Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1],
            'msg': 'succ.'
        })
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return response.Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })     



# class LoginView(KnoxLoginView):
#     permission_classes = (AllowAny, )
    
#     def post(self, request, format=None):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginView, self).post(request, format=None)

    # def post(self, request, *args, **kwargs):
    #     serializer = LoginSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data
    #     return response.Response({
    #         "user": UserSerializer(user, context=self.get_serializer_context()).data,
    #         "token": AuthToken.objects.create(user)[1]
    #     })

# class LogoutView(KnoxLogoutView):
#     permission_classes = [
#         IsAuthenticated
#     ]
#     authentication_classes = (TokenAuthentication, SessionAuthentication)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         logout(request, user)
#         return super(LogoutView, self).post(request, format=None)