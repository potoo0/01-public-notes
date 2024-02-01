from celery.schedules import crontab
# from datetime import timedelta


broker_url = 'redis://localhost:6379/5'
result_backend = 'redis://localhost:6379/6'

imports = ('tasks',)

worker_concurrency = 2

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'

# task 内部 stdout 是否重定向到 log
worker_redirect_stdouts = True

# beat 设置
redbeat_redis_url = "redis://localhost:6379/7"
beat_scheduler = 'redbeat.RedBeatScheduler'
beat_max_loop_interval = 5
beat_schedule = {
    'purge_updatedata_schedule': {
        'task': 'tasks.list_schedule',
        # 'schedule': timedelta(seconds=5),  # debug
        'schedule': crontab(minute=59, hour=23),
        'args': ()
    },
}
