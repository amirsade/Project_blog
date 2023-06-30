from .views import *
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('ticket/', TicketView.as_view(), name='ticket'),
    path('posts/<pk>', PostDetailView.as_view(), name='post_detail'),
    path('posts/<post_id>/comments', CommentView.as_view(), name='post_comment'),
    path('posts-api/', PostListApiView.as_view(), name='posts_api'),
    path('posts-create-api/', PostCreateApiView.as_view(), name='post_create')


]