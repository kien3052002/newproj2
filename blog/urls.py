from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('search/', views.post_search, name='post_search'),
    path('<slug:post>/', views.post_single, name='post_single'),
    path('like/<slug:post>', views.like, name='like_post'),
    path('<slug:post>/edit', views.edit_post, name='edit_post'),
    path('<slug:post>/delete', views.delete_post, name='delete_post')
]
