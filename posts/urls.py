from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='posts_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('dark-mode/', views.dark_mode, name='dark_mode'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('signup/', views.signup, name='signup'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
]
