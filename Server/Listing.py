from threading import Lock


class SingletonMeta(type):

    _instans = None
    _lock = Lock()

    def __call__(self, *args, **kwargs):
        with self._lock:
            if not self._instans:
                self._instans = super().__call__(*args, **kwargs)
        return self._instans


class Lists(metaclass=SingletonMeta):
    robot_state = {
        "A": "Star",
        "B": "Input"
    }
    task_list_robot = []
    list_cal = []
    task_list_sort = []
    list_qr_flag = [False, False, False]