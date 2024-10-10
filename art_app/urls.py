from django.urls import path
from .import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, CommentDeleteView, CommentUpdateView
urlpatterns = [
    path('', PostListView.as_view(),  name ='index'),
    path('user/<username>/', UserPostListView.as_view(),  name ='user-post'),
    path('post<int:pk>/comment_delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post<int:pk>/comment_update/', CommentUpdateView.as_view(), name='comment-update'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('search/', views.search, name='search')


]