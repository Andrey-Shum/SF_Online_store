from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Здесь мы импортировали класс формы, который предоставляет allauth, а также модель групп.
from allauth.account.forms import SignupForm
# from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives, mail_managers

# from django.core.mail import send_mail


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

# class CustomSignupForm(SignupForm):
#     """
#     В первой строке метода мы вызываем этот же метод класса-родителя,
#     чтобы необходимые проверки и сохранение в модель User были выполнены.
#     Далее мы получаем объект модели группы с названием common users.
#     И в следующей строке мы добавляем нового пользователя в эту группу.
#     Обязательным требованием метода save() является возвращение объекта модели User по итогу выполнения функции.
#     """
#     def save(self, request):
#         user = super().save(request)
#         common_users = Group.objects.get(name="common users")
#         user.groups.add(common_users)
#         return user
#

# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#
#         send_mail(
#             subject='Добро пожаловать в наш интернет-магазин!',
#             message=f'{user.username}, вы успешно зарегистрировались!',
#             from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
#             recipient_list=[user.email],
#         )
#         return user
# Мы убрали старый код с добавлением пользователя в группу, чтобы он нас не отвлекал, и добавили отправку сообщения.
#
# Функция send_mail позволяет отправить письмо указанному получателю в recipient_list.
# В поле subject мы передаём тему письма, а в message — текстовое сообщение.
class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        subject = 'Добро пожаловать в наш интернет-магазин!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/products">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        return user


# Тема письма (subject), отправитель (from_email), и получатель (to) указываются точно так же,
# как и в предыдущем примере.
#
# А вот переменные text и html содержат две версии одного письма: текстовую и с HTML.
# В инициализатор класса EmailMultiAlternatives мы передаём текстовую версию,
# а html прикрепляем как альтернативный вариант письма. После чего отправляем составленное письмо.

"""
Если вы будете писать длинные сообщения с большим количеством разметки, 
то советуем вынести код в HTML-файл и с помощью функции render_to_string создать переменную с HTML-кодом. 
И уже эту переменную передать в attach_alternative. То есть, по сути, разработать шаблон не для выдачи в браузере, 
а для составления письма.
"""
