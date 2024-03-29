from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin # noqa
from django.urls import reverse_lazy
# from datetime import datetime, timedelta
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils import timezone
from django.shortcuts import render, redirect

from .forms import ProductForm
from .models import Product, Subscription, Category
from django.http import HttpResponse
from .filters import ProductFilter

from django.utils.translation import gettext as _  #  импортируем функцию для перевода
# from django.utils.translation import activate, get_supported_language_variant, LANGUAGE_SESSION_KEY

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef

from django.views.decorators.csrf import csrf_protect

from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

# from .tasks import hello, printer
from django.core.cache import cache  # импортируем наш кэш

import pytz #  импортируем стандартный модуль для работы с часовыми поясами


def Start_Padge(request):
    products = Product.objects.order_by('name')
    paginator = Paginator(products,  7)  # разбиваем на страницы по 7 объектов # noqa

    # Используйте request.GET.get('page') для получения значения параметра 'page' # noqa
    page_n = request.GET.get('page')
    try:
        products = paginator.page(page_n)
    except PageNotAnInteger:
        # Если страница не является целым числом, переходим на первую страницу
        products = paginator.page(1)
    except EmptyPage:
        # Если страница пустая, переходим на последнюю страницу
        products = paginator.page(paginator.num_pages)
    return render(request, 'flatpages/Start.html', {'products': products})


# class IndexView(View):
#     def get(self, request):
#         printer.delay(10)  # printer.delay(N = 10)
#         hello.delay()
#         return HttpResponse('Hello!')


# class IndexView(View):
#     def get(self, request):
#         printer.apply_async([10], countdown=5)
#         hello.delay()
#         return HttpResponse('Hello!')


# class IndexView(View):
#     def get(self, request):
#         printer.apply_async([10],
#                             eta=datetime.now() + timedelta(seconds=5))
#         hello.delay()
#         return HttpResponse('Hello!')


# class Index(View):
#     @staticmethod
#     def get(request):
#         string = _('Hello world')
#
#         return HttpResponse(string)


# class Index(View):
#     def get(self, request):
#         string = _('Hello world')
#
#         context = {
#             'string': string
#         }
#         return HttpResponse(render(request, 'index.html', context))


# class Index(View):
#     def get(self, request):
#         # Переводчики: Это сообщение появляется только на главной странице.
#         models = Product.objects.all()
#
#         context = {
#             'models': models,
#         }
#
#         return HttpResponse(render(request, 'index.html', context))


class Index(View):
    def get(self, request):
        # .  Переводчики: Это сообщение появляется только на главной странице.
        models = Product.objects.all()

        context = {
            'models': models,
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
            # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'index.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который
    #  и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/index')


class ProductsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Product
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'  # '-name' обратноя сортировка по имени
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    #
    # queryset = Product.objects.filtr(
    #     price_lt=300
    # ).order_by(
    #     'name'
    # )
    #
    template_name = 'products.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'products'
    paginate_by = 2  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ProductFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context


class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product.html
    template_name = 'product.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'product'
    queryset = Product.objects.all()

    # Переопределяем метод получения объекта, как ни странно кэш очень похож
    # на словарь, и метод get действует так же. Он забирает значение по ключу,
    # если его нет, то забирает None.
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
            return obj


# Для передачи параметров в этот код вам, но отправить GET
# с параметрами "number" и "multiplier".
# Например, если Вы хотите умножить число 5 на 3,
# Вам нужно отправить GET запрос на URL, где этот код обрабатывается,
# с параметрами вида: `?number=5&multiplier=3`.
# http://127.0.0.1:8000/multiply/?number=5&multiplier=3
def multiply(request):
    number = request.GET.get('number')
    multiplier = request.GET.get('multiplier')

    try:
        result = int(number) * int(multiplier)
        html = f"<html><body>{number}*{multiplier}={result}</body></html>"
    except (ValueError, TypeError):
        html = f"<html><body>Invalid input.</body></html>"

    return HttpResponse(html)


# def create_product(request):
#     form = ProductForm()  # если здесь стока то перейдёт в рендер форму
#     # с информацией об ошибке если после пользователю отправится пустая форма
#     # без информации об ошибке
#
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/products/')
#
#     return render(request, 'product_edit.html', {'form': form})

# Добавляем новое представление для создания товаров.
# class ProductCreate(LoginRequiredMixin, CreateView):
#     raise_exception = True
#     # Указываем нашу разработанную форму
#     form_class = ProductForm
#     # модель товаров
#     model = Product
#     # и новый шаблон, в котором используется форма.
#     template_name = 'product_edit.html'


class ProductCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_product',)
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


class ProductUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_product',)
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


class ProductDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_product',)
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        # обработка подписок отписок
        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    # Блок кода выполняет запрос к категориям и проверяет подписан ли текущий
    # пользователь на каждую категорию
    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
