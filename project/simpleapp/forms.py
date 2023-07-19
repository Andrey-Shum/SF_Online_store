from django import forms
from .models import Product

from django.core.exceptions import ValidationError


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             'name',
#             'description',
#             'category',
#             'price',
#             'quantity',
#         ]
#
#     def clean(self):
#         cleaned_data = super().clean()
#         description = cleaned_data.get("description")
#         if description is not None and len(description) < 20:
#             raise ValidationError({
#                 "description": "Описание не может быть менее 20 символов."
#             })
#
#         name = cleaned_data.get("name")
#         if name == description:
#             raise ValidationError("Описание не должно быть идентично названию.")
#
#         return cleaned_data
class ProductForm(forms.ModelForm):
    """ Мы убрали проверку на длину описания из метода, добавили поле в саму форму и в этом поле уже поставили
    ограничение на минимальную длину строки."""
    description = forms.CharField(min_length=20)

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'category',
            'price',
            'quantity',
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


# Помимо двух описанных методов валидации данных есть и третий,
# который можно встретить в Django-проектах.
# Он позволяет проверить с помощью функции данные одного конкретного поля.
# Раньше с помощью функции мы получали доступ к проверке всех полей вместе.
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             'name',
#             'description',
#             'category',
#             'price',
#             'quantity',
#         ]
#
#     def clean_name(self):
#         name = self.cleaned_data["name"]
#         if name[0].islower():
#             raise ValidationError(
#                 "Название должно начинаться с заглавной буквы"
#             )
#         return name

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'
#
# Для рабочих проектов советуем всё-таки потратить время и перечислить поля, чтобы не было ситуации,
# что вы добавили новое поле в модель, которое нельзя редактировать пользователям, а из-за fields = ‘__all__’
# это поле стало автоматически доступным для редактирования через форму.
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             'name',
#             'description',
#             'quantity',
#             'category',
#             'price',
#         ]

# Помимо того, что форма может быть автоматически сгенерирована на основе какой-либо модели,
# Django позволяет создавать их, просто указывая поля.

# class ProductForm(forms.Form):
#     name = forms.CharField(label='Name')
#     description = forms.CharField(label='Description')
#     quantity = forms.IntegerField(label='Quantity')
#     category = forms.ModelChoiceField(
#         label='Category', queryset=Category.objects.all(),
#     )
#     price = forms.FloatField(label='Price')
