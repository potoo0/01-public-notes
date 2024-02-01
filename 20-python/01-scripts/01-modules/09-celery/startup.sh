# windows 不支持默认的 pool(eventlet), 使用 gevent:
#    celery -A celery_worker.app worker -l info -P gevent

# celery 只有单个 worker 节点时可以直接加参数 -B, 同时 beat:
#       celery -A celery_worker.app worker -l info -B
#   否则单独启动: celery -A celery_worker.app beat -l info

# 单节点，加 -B 同时启动 beat
# nohup celery -A celery_worker.app worker -l info -B >> ./log/celery.log 2>&1 &
celery -A celery_worker.app worker -l info -B
