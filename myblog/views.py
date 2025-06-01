from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Blog, Comment, Like
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, BlogSerializer, CommentSerializer, BlogSerializer
from django.shortcuts import render
from rest_framework.permissions import AllowAny

def blog_form_view(request):
    return render(request, 'blog.html')


def index(request):
    return render(request, 'home.html')

def dashboard(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.filter(author=request.user)
        return render(request, 'dashboard.html', {'blogs': blogs})
    return render(request, 'login-form.html')


def register_form_view(request):
    return render(request, 'register_form.html')

def login_form_view(request):
    return render(request, 'login_form.html')


class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # Deletes the token from DB
        return Response({"message": "Logged out successfully"})


class BlogCreateAPIView(generics.CreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# class LoginAPI(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginAPI(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            # Optional: log the user in for session-based auth
            login(request, user)

            # Generate or retrieve token
            token, _ = Token.objects.get_or_create(user=user)

            return JsonResponse({'token': token.key})  # <-- THIS is the fix
        return JsonResponse(serializer.errors, status=400)

class BlogListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

        

# class BlogViewSet(viewsets.ModelViewSet):
#     serializer_class = BlogSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         if self.action == 'retrieve':
#             return Blog.objects.filter(author=self.request.user)
#         return Blog.objects.all()

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     def perform_update(self, serializer):
#         if self.request.user != serializer.instance.author:
#             raise PermissionDenied("You can't edit this post.")
#         serializer.save()

#     def destroy(self, request, *args, **kwargs):
#         post = self.get_object()
#         if post.author != request.user:
#             return Response({'error': 'Only the author can delete this post.'}, status=status.HTTP_403_FORBIDDEN)
#         return super().destroy(request, *args, **kwargs)

class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        Like.objects.get_or_create(user=request.user, blog=blog)
        return Response({'message': 'Post liked'})

class CommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow the user to update/delete their own blogs
        return self.queryset.filter(author=self.request.user)