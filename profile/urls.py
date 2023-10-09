from django.urls import path, re_path

from profile import views

urlpatterns = [
    re_path(r'^(?P<username>[\w.@+-]+)/$', views.profile, name='profile'),
]