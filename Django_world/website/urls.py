"""Website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # Home
    url(r'^$', views.root, name='root'),
    url(r'^home/?$', views.home, name='home'),

    # Accounts
    url(r'^accounts/register$', views.register, name='register'),

    # Formulaires de création
    url(r'^new/game/?$', views.create_game, name='new_game'),
    url(r'^new/game/(\d+)/?$', views.game, name='game'),
    url(r'new/activity/?$', views.new_activity, name='new_activity'),

    # Partie en cours
    url(r'playing/(\d+)/?$', views.playing, name='playing'),
]
