import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Macdonalds.settings')


app = Celery('Macdonalds')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://localhost:6379'

app.autodiscover_tasks()

# Периодические задачи
# app.conf.beat_schedule = {
#     'print_every_5_seconds': {
#         'task': 'board.tasks.printer',
#         'schedule': 5, # каждые 5 секунд
#         'args': (5,), # передача аргумента в функцию tasks.print
#     },
# }


# app.conf.beat_schedule = {
#     'action_every_monday_8am': {
#         'task': 'action',
#         'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
#         'args': (agrs),
#     },
# }


app.conf.beat_schedule = {
    'clear_board_every_minute': {
        'task': 'board.tasks.clear_board', # здесь указана задача, которую мы написали в файле tasks
        'schedule': crontab(),
    },
}