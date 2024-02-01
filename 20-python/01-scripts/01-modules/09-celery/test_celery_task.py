# Vscode Jupyter code cells
# add new code cell, input # %%
# add new markdown cell, input '# %% [markdown]'
# %% [markdown]
# ## 1. send task

# %%
from celery.result import AsyncResult

from celery_worker import app


# %%
task = app.send_task('tasks.add_task', args=(1, 3))


# %%
task.state, task.task_id
if task.state == 'SUCCESS':
    print(f'task res: {task.get()}')


# %%
# get task by id
res = AsyncResult(task.task_id, app=app)
res.state

# %% [markdown]
# ## 2. add periodic task

# %%
from pandas import to_timedelta  # noqa
from celery.schedules import schedule  # noqa
from redbeat import RedBeatSchedulerEntry as Entry  # noqa

from celery_worker import app  # noqa


# %%
# add periodic task
sch = schedule(run_every=to_timedelta('10sec'))
entry = Entry(name='test01', task='tasks.add_task',
              schedule=sch, args=(5, 10), app=app)
entry.save()

print(entry.key, "->", entry.schedule)

# %%
# run periodic task now
task = app.send_task(entry.task, args=entry.args, kwargs=entry.kwargs)
task.state

# %%
# delete task
entry_ret = Entry.from_key(entry.key, app=app)
entry_ret.delete()


# %%
# get all periodic task
#   暂时没有集成的 api, 可通过查 redis 获取所有定时任务
from redbeat import schedulers  # noqa

# 获取 redis 连接
redis = schedulers.get_redis(app)
# 获取调度器配置
conf = schedulers.RedBeatConfig(app)
# 根据调度器配置的 key 获取此有序集合的所有成员, 此成员就是配置的定时任务的 key
keys = redis.zrange(conf.schedule_key, 0, -1)
# 根据任务的 key 获取任务
entries = [schedulers.RedBeatSchedulerEntry.from_key(key, app=app)
           for key in keys]


# %%
# purge periodic task
for entry in entries:
    entry.delete()

# %%
