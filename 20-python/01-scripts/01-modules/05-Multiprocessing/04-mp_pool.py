import multiprocessing as mp


def job(x):
    return x * x


def multicore():
    # 参数processes，启用的核的数目。默认是全部的核
    pool = mp.Pool(processes=2)
    print(pool.map(job, range(2)))

    batch_task = pool.map_async(job, range(2))
    batch_task.wait()
    print(batch_task.get())

    res_apply = pool.apply_async(job, (2,))
    res_apply.wait()
    print(res_apply.get())


if __name__ == '__main__':
    multicore()
