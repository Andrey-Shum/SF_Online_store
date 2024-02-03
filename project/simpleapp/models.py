from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache


# специальная функция reverse, которая позволяет нам указывать
# не путь вида /products/…, а название пути.


# Товар для нашей витрины
class Product(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,  # названия товаров не должны повторяться
    )
    price = models.FloatField(validators=[MinValueValidator(0.0)],)
    # price = models.FloatField(validators=[MinValueValidator(0.0, 'Price should be >= 0.0')])
    quantity = models.IntegerField(validators=[MinValueValidator(0)],)
    # quantity = models.IntegerField(validators=[MinValueValidator(0, 'Quantity should be >= 0')])
    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='products',  # все продукты в категории будут доступны через поле products
    )
    # category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f'{self.name.title()}: {self.description[:10]} ({self.price})'

    # Django не знает, какую страницу нужно открыть после создания товара.
    # Мы можем убрать проблему, добавив метод get_absolute_url в модель.
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])

    # def get_absolute_url(self):
    #     # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
    #     return f'/products/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
