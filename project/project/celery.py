import os
from celery import Celery
# В первую очередь мы импортируем библиотеку для взаимодействия с операционной
# системой и саму библиотеку Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
# мы связываем настройки Django с настройками Celery через переменную окружения.
app = Celery('project')
# создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации
app.config_from_object('django.conf:settings', namespace='CELERY')
# Указываем пространство имен, чтобы Celery сам находил все необходимые
# настройки в общем конфигурационном файле settings.py. Он их будет искать
# по шаблону «CELERY_***»
app.autodiscover_tasks()
# Указываем Celery автоматически искать задания в файлах tasks.py каждого
# приложения проекта.
