from django.urls import path

from item import views

app_name = 'item'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('new/', views.NewItem, name='new_item'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.EditItem, name='edit_item'),
    path('', views.items, name='items'),
    ]