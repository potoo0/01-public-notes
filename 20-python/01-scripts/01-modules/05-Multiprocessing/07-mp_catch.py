from multiprocessing import Process, Queue, Value, Pipe
import time
from addon.camera import camera
import cv2
import traceback


class myProcess(Process):
    def __init__(self, *args, **kw):
        Process.__init__(self, *args, **kw)
        self._pconn, self._cconn = Pipe()
        self._exception = None

    def run(self):
        try:
            Process.run(self)
            self._cconn.send(None)
        except Exception as e:
            tb = traceback.format_exc()
            self._cconn.send((e, tb))

    @property
    def exception(self):
        if self._pconn.poll():
            # .poll(): return whether there is any data avaliable to read
            self._exception = self._pconn.recv()
        return self._exception


def job1(initFinish, queue):
    cam = camera(0)

    initFinish.value += 1
    while True:
        if not initFinish.value == 3:
            continue

        print('job1 running' + '_' * 8)
        frame = cam.getFrame()
        queue.put(frame)
        time.sleep(0.5)

        if queue.qsize() > 3:
            queue.clear()


def job2(initFinish, queue):
    cnt = 0

    initFinish.value += 1
    while True:
        if not initFinish.value == 3:
            continue

        print('job2 running' + '+' * 8)
        time.sleep(0.5)

        if queue.empty():
            continue

        frame = queue.get()
        cv2.namedWindow("classification")
        cv2.imshow('classification', frame)
        cv2.waitKey(10)

        cnt += 1
        if cnt > 5:
            raise ChildProcessError('error in job2')


def job3(initFinish, queue):
    initFinish.value += 1
    while True:
        if not initFinish.value == 3:
            continue

        print('job3 running' + '*' * 8)
        time.sleep(4)


if __name__ == '__main__':
    try:
        queue = Queue()
        initFinish = Value('b', 0)  # 共享内存，用于让进程1 等到进程2 开始正常工作

        proceesses = []

        proceesses.append(
            myProcess(target=job1,
                      args=(initFinish, queue))
        )
        proceesses.append(
            myProcess(target=job2,
                      args=(initFinish, queue))
        )
        proceesses.append(
            myProcess(target=job3,
                      args=(initFinish, queue))
        )

        for p in proceesses:
            p.daemon = True
        for p in proceesses:
            p.start()

        while True:
            for p in proceesses:
                if p.exception:
                    raise ChildProcessError(p.exception)

    except Exception as e:
        for p in proceesses:
            p.terminate()
        print('-----------end-----------')
        print(e)
