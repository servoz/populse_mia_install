import sys
import subprocess


def install_package(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.call([sys.executable, '-m', 'pip', 'install', '--user', package])


def install_pyqt():
    """
    Installs PyQt5 if not already installed
    """
    install_package('PyQt5')


def install_yaml():
    """
    Installs pyyaml if not already installed.
    This package is special because it is called "pyyaml" in the PyPi world but "yaml" in the Python world.
    """
    import importlib
    try:
        importlib.import_module('yaml')
    except ImportError:
        subprocess.call([sys.executable, '-m', 'pip', 'install', '--user', 'pyyaml'])


if __name__ == '__main__':

    install_pyqt()
    install_yaml()

    try:
        import yaml
    except ImportError:  # giving a last chance to install pyyaml
        subprocess.call([sys.executable, '-m', 'pip', 'install', '--user', 'pyyaml'])

    try:
        from PyQt5 import QtWidgets
    except ImportError:  # giving a last chance to install PyQt5
        subprocess.call([sys.executable, '-m', 'pip', 'install', '--user', 'PyQt5'])

    # Removing PyQt5 from the sys modules to avoid conflicts
    if 'PyQt5' in sys.modules.keys():
        del sys.modules['PyQt5']

    try:
        from PyQt5 import QtWidgets
        import yaml
    except ImportError:
        print('\n\nPython package environment has not been correctly updated.\n\nPlease relaunch the following command:'
              ' python3 install_mia.py')

    from PyQt5 import QtWidgets
    from mia_install_widget import MIAInstallWidget

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
