import sys


def install_package(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])


def install_pyqt():
    """
    Installs PyQt5 if not already installed
    """
    install_package('pyqt5')


if __name__ == '__main__':

    install_pyqt()

    from PyQt5 import QtWidgets
    from .mia_install_widget import MIAInstallWidget

    app = QtWidgets.QApplication(sys.argv)
    mia_install_widget = MIAInstallWidget()

    # Setting the window to the middle of the screen
    frame_gm = mia_install_widget.frameGeometry()
    screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
    center_point = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
    frame_gm.moveCenter(center_point)
    mia_install_widget.move(frame_gm.topLeft())

    mia_install_widget.show()
    app.exec()
