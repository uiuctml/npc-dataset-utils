import enum
import PyQt5.QtCore
import PyQt5.QtWidgets

class CorruptionAlgorithm(enum.Enum):
    imagenet_c = 0
    color = 1

class CorruptionImageNetC(enum.Enum):
    gaussian_noise = 0
    shot_noise = 1
    impulse_noise = 2
    defocus_blur = 3
    glass_blur = 4
    motion_blur = 5
    zoom_blur = 6
    snow = 7
    frost = 8
    fog = 9
    brightness = 10
    contrast = 11
    elastic_transform = 12
    pixelate = 13
    jpeg_compression = 14

class LogLevel(enum.Enum):
    all = 6
    trace = 5
    debug = 4
    info = 3
    warn = 2
    error = 1
    fatal = 0
    off = -1

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class QLabelClickable(PyQt5.QtWidgets.QLabel):
    clicked_left = PyQt5.QtCore.pyqtSignal()
    clicked_right = PyQt5.QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mouse_position = None

        return

    def mousePressEvent(self, event):
        if event.button() == PyQt5.QtCore.Qt.LeftButton or event.button() == PyQt5.QtCore.Qt.RightButton:
            self.mouse_position = event.pos()

        return

    def mouseReleaseEvent(self, event):
        if self.mouse_position is not None and self.mouse_position in self.rect() and event.pos() in self.rect():
            if event.button() == PyQt5.QtCore.Qt.LeftButton:
                self.clicked_left.emit()

            if event.button() == PyQt5.QtCore.Qt.RightButton:
                self.clicked_right.emit()

        self.mouse_position = None

        return

class SplitBasis(enum.Enum):
    percentage = 0,
    statistics = 1
