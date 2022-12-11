from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='posts'),
    path('search/', views.search_post, name='search'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('add_post/', views.add_post, name='add_post'),
]