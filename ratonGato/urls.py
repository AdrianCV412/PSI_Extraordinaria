"""ratonGato URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from logic import views

urlpatterns = [
	path('', views.index, name='landing'),
    path('index/', views.index, name='landing'),
    path('admin/', admin.site.urls),
	path('login/', views.login_service, name='login'),
	path('signup/', views.signup_service, name='signup'),
	path('counter/', views.counter_service, name='counter'),
	path('join_game/', views.join_game_service, name='join_game'),
    path('join_game/<int:game_id>', views.join_game_service, name='join_game'),
	path('logout/', views.logout_service, name='logout'),
    path('get_move_service/', views.get_move_service, name='get_move'),
	path('create_game/', views.create_game_service, name='create_game'),
	path('select_game/', views.select_game_service, name='select_game'),
    path('select_game/<int:game_id>', views.select_game_service, name='select_game'),
    path('replay_game/', views.replay_game_service, name='replay_game'),
    path('replay_game/<int:game_id>', views.replay_game_service, name='replay_game'),
	path('play/', views.show_game_service, name='show_game'),
    path('move/', views.move_service, name='move'),
]
