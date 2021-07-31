from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('create/', views.post_create_view, name='post_create'),
    path('comment/<str:post_slug>/', views.comment_like_delete_view, name='post_comment'),
    path('comment/<str:post_slug>/<int:comment_id>/', views.comment_like_delete_view, name='comment_like_delete'),
    path('bookmark/<str:post_slug>/', views.post_detail_view, name='post_bookmark'),
    path('view/<str:post_slug>/', views.post_detail_view, name='post_detail'),
    path('edit/<str:post_slug>/', views.post_edit_delete_view, name='post_edit_delete'),
    path('edit/post/<str:post_slug>/', views.post_edit_view, name='post_edit'),
]