import sys, logging
from enum import Enum
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Log(Enum):
    """
    Logging level.
    """
    ERROR = 0
    WARNING = 1     
    INFO = 2
    DEBUG = 3

def emitLog(level, message, worker=None):
    """
    Multi porpose logging function.
    If called from current thread: Use logging to write message in log.
    If called from worker thread: Emit signal to send log message to application thread.

    Args:
        level (Log): Logging level.
        message (str): Logging message.
        worker (worker, optional): Worker thread. Defaults to None.
    """
    if "pytest" not in sys.modules:
        if(QThread.currentThread() == QApplication.instance().thread()):
            if level.value == Log.ERROR.value:
                logging.error(message)
            elif level.value == Log.WARNING.value:
                logging.warning(message)
            elif level.value == Log.INFO.value:
                logging.info(message)
            elif level.value == Log.DEBUG.value:
                logging.debug(message)
            else:
                logging.error("Invalid log level for message: " + message)
        else:
            worker.signals.log.emit(level, message)

class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.ERROR:   ("[%(levelname)-8s] %(message)s", "red"),
        logging.DEBUG:   ("[%(levelname)-8s] %(message)s", "green"),
        logging.INFO:    ("[%(levelname)-8s] %(message)s", "blue"),
        logging.WARNING: ("[%(levelname)-8s] %(message)s", "orange")
    }

    def format(self, record):
        last_fmt = self._style._fmt
        opt = CustomFormatter.FORMATS.get(record.levelno)
        if opt:
            fmt, color = opt
            self._style._fmt = "<font color=\"{}\">{}</font>".format(
                QColor(color).name(), fmt)
        res = logging.Formatter.format(self, record)
        self._style._fmt = last_fmt
        return res


class QPlainTextEditLogger(logging.Handler):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

        # Définir la taille de police du widget
        font = QFont()
        font.setPointSize(30) 
        self.widget.setFont(font)
        # Définir la feuille de style pour ajuster la taille du texte
        style_sheet = "font-size: {}px;".format(font.pointSize())
        self.widget.setStyleSheet(style_sheet)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendHtml(msg)
        # move scrollbar
        scrollbar = self.widget.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
