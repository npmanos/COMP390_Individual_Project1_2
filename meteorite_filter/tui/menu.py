

class MenuItem:
    def __init__(self, label: str, func_call, callback=None) -> None:
        self._label = label
        self._func_call = func_call
        self._callback = callback

    @property
    def label(self):
        return self._label

    def __call__(self) -> None:
        if self._callback is None:
            self._func_call()
        else:
            self._callback(self._func_call())

