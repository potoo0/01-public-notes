# start celery worker first: celery -A celery_worker.app worker -l info -B
celery -A celery_worker.app flower --address=0.0.0.0 --port=5566
