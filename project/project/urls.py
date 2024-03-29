"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

from simpleapp import views
from simpleapp.views import multiply, Index

urlpatterns = [
   path('i18n/', include('django.conf.urls.i18n')),  # подключаем встроенные эндопинты для работы с локализацией # noqa
   path('', views.Start_Padge, name='Start'),
   path('admin/', admin.site.urls),
   path('product/', include('django.contrib.flatpages.urls')),
   # Делаем так, чтобы все адреса из нашего приложения (simpleapp/urls.py)
   # подключались к главному приложению с префиксом products/.
   path('products/', include('simpleapp.urls')),
   path('index/', Index.as_view(), name='index'),  # страница с Hello world
   path('multiply/', multiply),  # для выполнения логики, связанной с умножением, при обращении пользователя по пути "multiply/" # noqa
   # Добавим urls приложения, с которым ранее работали в этом модуле — “django.contrib.auth”. # noqa
   # Django скажет, как обрабатывать запросы от пользователей по ссылкам, которые начинаются с /accounts/. # noqa
   # path('accounts/', include('django.contrib.auth.urls')),
   # path("accounts/", include("accounts.urls")),  # подключим urls приложения accounts # noqa
   path('accounts/', include('allauth.urls')),  # Оставили только allauth
]
