from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns=[
    # url('^$',views.welcome,name = 'welcome'),
    path('new/',views.create_post,name = 'new-pictures'),
    path('search/', views.search_results, name='search_results'),
    path('add-comment/<int:pk>/', views.add_comment, name='add-comment'),
    path('like/', views.like_post, name='like-post'),
    path('profile/', views.profile, name='profile'),
    


]