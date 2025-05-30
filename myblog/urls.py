from django.urls import path, include
from .views import RegisterAPI, LoginAPI
from .views import register_form_view
from .views import login_form_view
from .views import blog_form_view
from .views import index
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, LikeView, CommentView

router = DefaultRouter()
router.register(r'blogs', BlogViewSet, basename='blogs')

urlpatterns = [
    # path('', RegisterAPI.as_view(), name='register'),
    path('', index),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    # path('register-form/', register_view, name='register_form'),
    path('register-form/', register_form_view, name='register_form'),
    path('login-form/', login_form_view, name='login_form'),
    path('api/blogs/<int:pk>/like/', LikeView.as_view(), name='like'),
    path('api/comments/', CommentView.as_view(), name='comment'),
    path('api/', include(router.urls)),
    path('blog-form/', blog_form_view, name='blog_form'),

]
