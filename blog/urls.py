from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('search/', views.post_search, name='post_search'),
    path('<slug:post>/', views.post_single, name='post_single'),
    path('like/<slug:post>', views.like, name='like_post'),
    path('bookmark/<slug:post>', views.bookmark, name='bookmark_post'),
]
