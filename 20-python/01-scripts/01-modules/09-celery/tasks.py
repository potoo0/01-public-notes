from celery import Task
from redbeat import schedulers

from celery_worker import app


@app.task
def add_task(x, y):
    return x + y


@app.task(bind=True)  # bind=True, 将此任务函数绑定到实例, 即 self 可取 celery 实例
def list_schedule(self: Task):
    # 获取 redis 连接
    redis = schedulers.get_redis(self.app)
    # 获取调度器配置
    conf = schedulers.RedBeatConfig(self.app)
    # 根据调度器配置的 key 获取此有序集合的所有成员, 此成员就是配置的定时任务的 key
    keys = redis.zrange(conf.schedule_key, 0, -1)
    # 根据任务的 key 获取任务
    entries = [schedulers.RedBeatSchedulerEntry.from_key(key, app=self.app)
               for key in keys]
    print(entries)
