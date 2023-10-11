from django.urls import path, re_path

from profile import views

urlpatterns = [
    # path('choose_color/', views.choose_color, name='choose_color'),
    re_path(r'^(?P<username>[\w.@+-]+)/$', views.profile, name='profile'),
    path('profile/<str:username>/upvote/', views.upvote, name='upvote'),
    path('profile/<str:username>/downvote/', views.downvote, name='downvote'),
]