from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from .forms import MyAuthForm
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name="index"),
    path('login_user/', views.login_user, name="login"),
    path('gameMode/', views.gameMode, name="gameMode"),
    path('register_user/', views.register_user, name="register_user"),
    path('logout_user/', views.logout_user, name="logout"),
    path('kidMode/', views.kidMode, name="kidMode"),
    path('gameReport/', views.gameReport, name="gameReport"),
    path('proMode/', views.proMode, name="proMode"),
    path('kidMode/', views.button_kid, name="button_kid"),
    path('proMode/', views.button_pro, name="button_pro"),
    path('add_word/', views.add_word, name="add_word"),
] 