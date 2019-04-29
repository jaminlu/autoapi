#!coding: utf-8
from celery import platforms
from kombu import Exchange, Queue
#####celery config  ######
CELERY_BROKER_URL='amqp://rabbitmq:rabbitmq@10.10.61.55:5672/0'
CELERY_RESULT_BACKEND = 'amqp://rabbitmq:rabbitmq@10.10.61.55:5672/1'
#CELERY_RESULT_PERSISTENT=False
CELERY_RESULT_EXPIRE = 3600
BROKER_TRANSPORT_OPTIONS={'visibility_timeout':43200}
CELERY_BROKER_TRANSPORT_OPTIONS ={'visibility_time': 28800}
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_TASK_TIME_LIMIT= 5*60
BROKER_HEARTBEAT = 24 * 60 * 60
CELERY_ENABLE_UTC = True
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_EXCHANGE = 'default'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'


CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('taskpre', Exchange('taskpre'), routing_key='taskpre'),
    Queue('publish', Exchange('publish'), routing_key='publish'),
)

CELERY_ROUTES={
    'taskpre': {'queue':'taskpre', 'routing_key':'taskpre'},
    'publish': {'queue':'publish', 'routing_key':'publish'},
}
