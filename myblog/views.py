from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Blog, Comment, Like


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, BlogSerializer, CommentSerializer
from django.shortcuts import render

def blog_form_view(request):
    return render(request, 'blog.html')


def index(request):
    return render(request, 'home.html')

def register_form_view(request):
    return render(request, 'register_form.html')

def login_form_view(request):
    return render(request, 'login_form.html')


class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'retrieve':
            return Blog.objects.filter(author=self.request.user)
        return Blog.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("You can't edit this post.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response({'error': 'Only the author can delete this post.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

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