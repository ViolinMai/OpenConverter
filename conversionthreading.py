from PyQt6.QtCore import QObject, QThread, pyqtSignal

class ConverionsThreading(QObject):
    finished = pyqtSignal()
    success = pyqtSignal(object)
    error = pyqtSignal(str)
    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args
    def run(self):
        try:
            result = self.func(*self.args)
            self.success.emit(result)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()        