from django.urls import path
# Импортируем созданное нами представление
from .views import ProductsList, ProductDetail,  ProductCreate  # create_product

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', ProductsList.as_view()),
   #
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   # для создания ссылки вместо имени
   #
   # path('<int:pk>', ProductDetail.as_view()),
   # заменить на
   path('products/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
   # path('create/', create_product, name='product_create'),
   path('create/', ProductCreate.as_view(), name='product_create'),
]
