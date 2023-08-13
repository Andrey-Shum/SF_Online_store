from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Здесь мы импортировали класс формы, который предоставляет allauth, а также модель групп.
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


# В кастомизированном классе формы, в котором мы хотим добавлять пользователя в группу,
# нужно переопределить только метод save(), который выполняется при успешном заполнении формы регистрации.
class CustomSignupForm(SignupForm):
    """
    В первой строке метода мы вызываем этот же метод класса-родителя,
    чтобы необходимые проверки и сохранение в модель User были выполнены.
    Далее мы получаем объект модели группы с названием common users.
    И в следующей строке мы добавляем нового пользователя в эту группу.
    Обязательным требованием метода save() является возвращение объекта модели User по итогу выполнения функции.
    """
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        return user
