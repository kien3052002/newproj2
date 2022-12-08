from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('search/', views.post_search, name='post_search'),
    path('mybookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('<slug:post>/', views.post_single, name='post_single'),
    path('like/<slug:post>', views.like, name='like_post'),
    path('bookmark/<slug:post>', views.bookmark, name='bookmark_post'),
    path('hide/<slug:post>', views.hide_post, name='hide_post'),
    path('delete_cmt/<int:id>', views.delete_cmt, name='delete_comment'),

]
