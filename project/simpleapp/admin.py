from django.contrib import admin
from .models import Category, Product


# напишем уже знакомую нам функцию обнуления товара на складе
def nullfy_quantity(modeladmin, request, queryset):
    # все аргументы уже должны быть вам знакомы,
    # самые нужные из них это request — объект хранящий информацию о запросе
    # и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(quantity=0)


nullfy_quantity.short_description = 'Обнулить товары'
# описание для более понятного представления в админ панеле задаётся,
# как будто это объект.


# создаём новый класс для представления товаров в админке
class ProductAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями,
    # которые вы хотите видеть в таблице с товарами
    list_display = ('name', 'price', 'quantity')
    # оставляем только имя и цену товара
    list_filter = ('price', 'quantity', 'name')
    # добавляем примитивные фильтры в нашу админку
    search_fields = ('name', 'category__name')
    # тут всё очень похоже на фильтры из запросов в базу
    actions = [nullfy_quantity] # добавляем действия в список

# создаём новый класс для представления товаров в админке
# class ProductAdmin(admin.ModelAdmin):
#     # list_display — это список или кортеж со всеми полями,
#     # которые вы хотите видеть в таблице с товарами.
#     list_display = [
#         field.name for field in Product._meta.get_fields()
#     ]  # генерируем список имён всех полей для более красивого отображения


# # # создаём новый класс для представления товаров в админке
# class ProductAdmin(admin.ModelAdmin):
#     # list_display - это список или кортеж со всеми полями,
#     # которые вы хотите видеть в таблице с товарами
#     list_display = ('name', 'price')  # оставляем только имя и цену товара


# # создаём новый класс для представления товаров в админке
# class ProductAdmin(admin.ModelAdmin):
#     # list_display — это список или кортеж со всеми полями,
#     # которые вы хотите видеть в таблице с товарами
#     list_display = ('name', 'price', 'on_stock')
#     # оставляем только имя и цену товара
#     list_filter = ('price', 'quantity', 'name')
#     # добавляем примитивные фильтры в нашу админку


# # создаём новый класс для представления товаров в админке
# class ProductAdmin(admin.ModelAdmin):
#     # list_display — это список или кортеж со всеми полями,
#     # которые вы хотите видеть в таблице с товарами
#     list_display = (
#     'name', 'price', 'on_stock')  # оставляем только имя и цену товара
#     list_filter = (
#     'price', 'quantity', 'name')  # добавляем примитивные фильтры в нашу админку
#     search_fields = ('name', 'category__name')
#     # тут всё очень похоже на фильтры из запросов в базу


# Register your models here.
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
# admin.site.unregister(Product)  # разрегистрируем наши товары
