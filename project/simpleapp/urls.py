from django.urls import path
# Импортируем созданное нами представление
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
   # path('', IndexView.as_view()),
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   # path('', ProductsList.as_view()),
   path('', ProductsList.as_view(), name='product_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   # для создания ссылки вместо имени
   #
   # path('<int:pk>', ProductDetail.as_view()),
   # заменить на
   path('<int:pk>/', ProductDetail.as_view(), name='product_detail'),
   # path('<int:pk>/', cache_page(60*10)(ProductDetail.as_view()), name='product_detail'),
   # Добавим кэширование на детали товара. Раз в 10 минут товар будет записываться в кэш для экономии ресурсов.

   # path('create/', create_product, name='product_create'),
   path('create/', ProductCreate.as_view(), name='product_create'),
   path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
   path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]
