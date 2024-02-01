from celery import Celery

import celeryconf


app = Celery(__name__)
app.config_from_object(celeryconf)
