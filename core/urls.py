from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views
from .forms import LoginForm
from .views import request_new_activation_link

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('terms_of_use/', views.terms_of_use, name='terms_of_use'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),


    path('request_new_activation_link/', request_new_activation_link, name='request_new_activation_link'),
    path('request_new_activation_link/<str:email>/', request_new_activation_link, name='request_new_activation_link_with_email'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="core/password_reset.html"), name='password_reset'),

    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name="core/password_sent.html"), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="core/password_rest_form.html"), name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="core/password_reset_done.html"), name='password_reset_complete'),
    ]