import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcdonalds.settings')
 
app = Celery('mcdonalds')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# В этом же файле мы можем добавить и само расписание, по которому должны будут запускаться задачи.
# Само расписание представляет собой словарь словарей. Ключ основного словаря — это имя периодической задачи.
# Значение — это словарь с параметрами периодической задачи — сама задача, которая будет выполняться, аргументы,
# а также параметры расписания.
# app.conf.beat_schedule = {
#     'action_every_30_seconds': {
#         'task': 'tasks.action',
#         'schedule': 30,
#         'args': ("some_arg"),
#     },
# }

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'board.tasks.printer',
        'schedule': 5,
        'args': (5,),
    },
}

# app.conf.beat_schedule = {
#     'action_every_monday_8am': {
#         'task': 'action',
#         'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
#         'args': (agrs),
#     },
# }

app.conf.beat_schedule = {
    'clear_board_every_minute': {
        'task': 'board.tasks.clear_old',
        'schedule': crontab(),
    },
}
