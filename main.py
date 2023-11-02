import sys, signal
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet
from src import *

def main():
    """
    Main function.
    """
    def signalHandler(*args):
        """
        Handler for the SIGINT signal.
        """
        sys.stderr.write("\r")
        if QMessageBox.question(None,
                                "",
                                "Are you sure you want to quit?",
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No) == QMessageBox.Yes:
            window.signalHandler()
            _app.quit()

    # Create application
    _app = QApplication(sys.argv)
    window = Application()
    apply_stylesheet(_app, theme="light_blue.xml", extra={'density_scale': '10',})

    # Signal handler
    signal.signal(signal.SIGINT, signalHandler)

    # Allow Python interpreter to run every few seconds to handle signals
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None) # Let the interpreter run each 500 ms.

    # Run application
    sys.exit(_app.exec_())


if __name__ == "__main__":
    main()