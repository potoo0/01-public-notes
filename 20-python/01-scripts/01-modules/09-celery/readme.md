caution:
>
>  1. windows don't support default pool implementation: eventlet, use gevent instead.
>  2. when run only one worker node, could embed beat inside the worker by enabling the workers -B option.

start worker:

```bash
celery -A celery_worker worker -l info -P gevent
```

start beat:

```bash
celery -A celery_worker beat -l info
```

start worker and embed beat(only one worker node):

```bash
celery -A celery_worker worker -l info -P gevent -B
```
