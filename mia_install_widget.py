import os
import sys
import yaml
import shutil
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore


class MIAInstallWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        # Labels
        self.top_label_text = 'Welcome to Populse_MIA installation.'
        self.top_label = QtWidgets.QLabel(self.top_label_text)

        self.top_label_font = QtGui.QFont()
        self.top_label_font.setBold(True)
        self.top_label.setFont(self.top_label_font)

        h_box_top_label = QtWidgets.QHBoxLayout()
        h_box_top_label.addStretch(1)
        h_box_top_label.addWidget(self.top_label)
        h_box_top_label.addStretch(1)

        self.middle_label_text = 'Please select an installation path and a folder to store your future projects.'

        self.middle_label = QtWidgets.QLabel(self.middle_label_text)
        h_box_middle_label = QtWidgets.QHBoxLayout()
        h_box_middle_label.addStretch(1)
        h_box_middle_label.addWidget(self.middle_label)
        h_box_middle_label.addStretch(1)

        # Groupbox
        self.groupbox = QtWidgets.QGroupBox()

        mia_path_default = os.path.join(os.path.expanduser('~'), '.populse_mia')

        self.mia_path_label = QtWidgets.QLabel("Populse_MIA installation path:")
        self.mia_path_choice = QtWidgets.QLineEdit(mia_path_default)
        self.mia_path_browse = QtWidgets.QPushButton("Browse")
        self.mia_path_browse.clicked.connect(self.browse_mia_path)

        self.mia_path_info = QtWidgets.QPushButton(" ? ")
        self.mia_path_info.setFixedHeight(27)
        self.mia_path_info.setFixedWidth(27)
        self.mia_path_info.setStyleSheet("background-color:rgb(150,150,200)")
        rect = QtCore.QRect(4, 4, 17, 17)
        region = QtGui.QRegion(rect, QtGui.QRegion.Ellipse)
        self.mia_path_info.setMask(region)
        tool_tip_message = "Two folders will be created in the selected folder:\n- populse_mia: containing " \
                           "populse_mia's configuration and resources files.\n- MRIFileManager: containing " \
                           "the file converter used in Populse_MIA."
        self.mia_path_info.setToolTip(tool_tip_message)

        h_box_mia_path = QtWidgets.QHBoxLayout()
        h_box_mia_path.addWidget(self.mia_path_choice)
        h_box_mia_path.addWidget(self.mia_path_browse)
        h_box_mia_path.addWidget(self.mia_path_info)

        v_box_mia_path = QtWidgets.QVBoxLayout()
        v_box_mia_path.addWidget(self.mia_path_label)
        v_box_mia_path.addLayout(h_box_mia_path)

        projects_path_default = ''  # setting a default value for the projects?

        self.projects_path_label = QtWidgets.QLabel("Populse_MIA projects path:")
        self.projects_path_choice = QtWidgets.QLineEdit(projects_path_default)
        self.projects_path_browse = QtWidgets.QPushButton("Browse")
        self.projects_path_browse.clicked.connect(self.browse_projects_path)

        self.projects_path_info = QtWidgets.QPushButton(" ? ")
        self.projects_path_info.setFixedHeight(27)
        self.projects_path_info.setFixedWidth(27)
        self.projects_path_info.setStyleSheet("background-color:rgb(150,150,200)")
        rect = QtCore.QRect(4, 4, 17, 17)
        region = QtGui.QRegion(rect, QtGui.QRegion.Ellipse)
        self.projects_path_info.setMask(region)
        tool_tip_message = 'A "projects" folder will be created in this specified folder.'
        self.projects_path_info.setToolTip(tool_tip_message)

        h_box_projects_path = QtWidgets.QHBoxLayout()
        h_box_projects_path.addWidget(self.projects_path_choice)
        h_box_projects_path.addWidget(self.projects_path_browse)
        h_box_projects_path.addWidget(self.projects_path_info)

        v_box_projects_path = QtWidgets.QVBoxLayout()
        v_box_projects_path.addWidget(self.projects_path_label)
        v_box_projects_path.addLayout(h_box_projects_path)

        v_box_paths = QtWidgets.QVBoxLayout()
        v_box_paths.addLayout(v_box_mia_path)
        v_box_paths.addLayout(v_box_projects_path)

        self.groupbox.setLayout(v_box_paths)

        # Clinical mode groupbox
        self.clinical_mode_group_box = QtWidgets.QGroupBox('Operating mode:')

        self.clinical_mode_push_button = QtWidgets.QRadioButton('Clinical mode')
        self.research_mode_push_button = QtWidgets.QRadioButton('Research mode')

        v_box_clinical_mode = QtWidgets.QVBoxLayout()
        v_box_clinical_mode.addWidget(self.clinical_mode_push_button)
        v_box_clinical_mode.addWidget(self.research_mode_push_button)

        self.clinical_mode_group_box.setLayout(v_box_clinical_mode)

        h_box_clinical_mode = QtWidgets.QHBoxLayout()
        h_box_clinical_mode.addWidget(self.clinical_mode_group_box)
        h_box_clinical_mode.addStretch(1)

        # Push buttons
        self.push_button_install = QtWidgets.QPushButton("Install")
        self.push_button_install.clicked.connect(self.install)

        self.push_button_cancel = QtWidgets.QPushButton("Cancel")
        self.push_button_cancel.clicked.connect(self.close)

        h_box_buttons = QtWidgets.QHBoxLayout()
        h_box_buttons.addStretch(1)
        h_box_buttons.addWidget(self.push_button_install)
        h_box_buttons.addWidget(self.push_button_cancel)

        # Final layout
        self.global_layout = QtWidgets.QVBoxLayout()
        self.global_layout.addLayout(h_box_top_label)
        self.global_layout.addLayout(h_box_middle_label)
        self.global_layout.addWidget(self.groupbox)
        self.global_layout.addLayout(h_box_clinical_mode)
        self.global_layout.addLayout(h_box_buttons)

        self.setLayout(self.global_layout)
        self.setWindowTitle("Populse_MIA installation")

    def browse_mia_path(self):
        folder_name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a folder where to install Populse_MIA')
        if folder_name:
            self.mia_path_choice.setText(folder_name)

    def browse_projects_path(self):
        folder_name = QtWidgets.QFileDialog.\
            getExistingDirectory(self, "Select a folder where to store Populse_MIA's projects")
        if folder_name:
            self.projects_path_choice.setText(folder_name)

    def set_new_layout(self):
        # Reparenting the layout to a temporary widget
        QtWidgets.QWidget().setLayout(self.global_layout)

        # Setting a new layout
        self.mia_installing_label = QtWidgets.QLabel("Populse_MIA is getting installed. Please wait.")
        self.mia_installing_label.setFont(self.top_label_font)

        h_box_top_label = QtWidgets.QHBoxLayout()
        h_box_top_label.addStretch(1)
        h_box_top_label.addWidget(self.mia_installing_label)
        h_box_top_label.addStretch(1)

        self.status_label = QtWidgets.QLabel("Status:")

        self.check_box_mia = QtWidgets.QCheckBox("Copying populse_mia")

        self.check_box_mri_conv = QtWidgets.QCheckBox("Copying MRIFileManager")

        self.check_box_config = QtWidgets.QCheckBox("Writing config file")

        self.check_box_pkgs = QtWidgets.QCheckBox("Installing Python packages (may take a few minutes)")

        self.v_box_install_status = QtWidgets.QVBoxLayout()
        self.v_box_install_status.addLayout(h_box_top_label)
        self.v_box_install_status.addWidget(self.status_label)
        self.v_box_install_status.addWidget(self.check_box_mia)
        self.v_box_install_status.addWidget(self.check_box_mri_conv)
        self.v_box_install_status.addWidget(self.check_box_config)
        self.v_box_install_status.addWidget(self.check_box_pkgs)
        self.v_box_install_status.addStretch(1)

        self.setLayout(self.v_box_install_status)

        QtWidgets.QApplication.processEvents()

    def last_layout(self):
        # Reparenting the layout to a temporary widget
        QtWidgets.QWidget().setLayout(self.v_box_install_status)

        # Setting a new layout
        self.mia_installed_label = QtWidgets.QLabel("Populse_MIA has been correctly installed.")
        self.mia_installed_label.setFont(self.top_label_font)

        h_box_top_label = QtWidgets.QHBoxLayout()
        h_box_top_label.addStretch(1)
        h_box_top_label.addWidget(self.mia_installed_label)
        h_box_top_label.addStretch(1)

        mia_label_text = "- populse_mia path: {0}".format(self.mia_path)
        projects_label_text = "- projects path: {0}".format(self.projects_save_path)
        mri_conv_label_text = "- MRIFileManager path: {0}".format(self.mri_conv_path)
        operating_mode_label_text = "Populse_MIA has been installed with {0} mode.".format(self.operating_mode)

        mia_label = QtWidgets.QLabel(mia_label_text)
        projects_label = QtWidgets.QLabel(projects_label_text)
        mri_conv_label = QtWidgets.QLabel(mri_conv_label_text)
        operating_mode_label = QtWidgets.QLabel(operating_mode_label_text)

        mia_command_label_text = "To launch Populse_MIA, execute this command line: python3 -m populse_mia"
        mia_command_label = QtWidgets.QLabel(mia_command_label_text)
        mia_command_label.setFont(self.top_label_font)

        button_quit = QtWidgets.QPushButton("Quit")
        button_quit.clicked.connect(self.close)

        h_box_button = QtWidgets.QHBoxLayout()
        h_box_button.addStretch(1)
        h_box_button.addWidget(button_quit)

        v_box_last_layout = QtWidgets.QVBoxLayout()
        v_box_last_layout.addLayout(h_box_top_label)
        v_box_last_layout.addStretch(1)
        v_box_last_layout.addWidget(mia_label)
        v_box_last_layout.addWidget(projects_label)
        v_box_last_layout.addWidget(mri_conv_label)
        v_box_last_layout.addStretch(1)
        v_box_last_layout.addWidget(operating_mode_label)
        v_box_last_layout.addStretch(1)
        v_box_last_layout.addWidget(mia_command_label)
        v_box_last_layout.addStretch(1)
        v_box_last_layout.addLayout(h_box_button)

        self.setLayout(v_box_last_layout)

        QtWidgets.QApplication.processEvents()

    def install(self):

        self.folder_exists_flag = False

        # Checking which operating mode has been selected
        if self.clinical_mode_push_button.isChecked():
            use_clinical_mode = "yes"
            self.operating_mode = "clinical"
        else:
            use_clinical_mode = "no"
            self.operating_mode = "research"

        # Creating the .populse_mia folder if it does not exists
        home_path = os.path.expanduser('~')
        dot_mia_path = os.path.join(home_path, '.populse_mia')

        if not os.path.isdir(dot_mia_path):
            os.mkdir(dot_mia_path)

        # Checking that the specified paths are correct
        mia_path = self.mia_path_choice.text()
        if not os.path.isdir(mia_path):
            message = "The selected path for Populse_MIA must be an existing folder"
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Populse_MIA path is not valid")
            msg.setInformativeText(message)
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.buttonClicked.connect(msg.close)
            msg.exec()
            return

        projects_path = self.projects_path_choice.text()
        if not os.path.isdir(projects_path):
            message = "The selected path for Populse_MIA's projects must be an existing folder"
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Populse_MIA's projects path is not valid")
            msg.setInformativeText(message)
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.buttonClicked.connect(msg.close)
            msg.exec()
            return

        if os.path.isdir(os.path.join(mia_path, 'populse_mia')):
            message = 'A "populse_mia" folder already exists in the selected path for the populse_mia install'
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText(message)
            self.msg.setInformativeText('By pressing "OK", this folder and its content will be removed.')
            self.msg.setWindowTitle("Warning")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.msg.buttonClicked.connect(self.ok_or_abort)
            self.msg.exec()

        # If the user has clicked on "Cancel" the installation is aborted
        if self.folder_exists_flag:
            return
        else:
            shutil.rmtree(os.path.join(mia_path, 'populse_mia'), ignore_errors=True)

        if os.path.isdir(os.path.join(mia_path, 'MRIFileManager')):
            message = 'A "MRIFileManager" folder already exists in the selected path for the MRIFileManager install'
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText(message)
            self.msg.setInformativeText('By pressing "OK", this folder and its content will be removed.')
            self.msg.setWindowTitle("Warning")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.msg.buttonClicked.connect(self.ok_or_abort)
            self.msg.exec()

        # If the user has clicked on "Cancel" the installation is aborted
        if self.folder_exists_flag:
            return
        else:
            shutil.rmtree(os.path.join(mia_path, 'MRIFileManager'), ignore_errors=True)

        if os.path.isdir(os.path.join(projects_path, 'projects')):
            message = 'A "projects" folder already exists in the selected path for the projects'
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText(message)
            self.msg.setWindowTitle("Warning")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.msg.buttonClicked.connect(self.ok_or_abort)
            self.msg.exec()

        # If the user has clicked on "Cancel" the installation is aborted
        if self.folder_exists_flag:
            return

        self.mia_path = os.path.abspath(os.path.join(mia_path, 'populse_mia'))
        self.projects_save_path = os.path.abspath(os.path.join(projects_path, 'projects'))
        self.mri_conv_path = os.path.abspath(os.path.join(mia_path, 'MRIFileManager'))

        self.set_new_layout()

        # Creating a "projects" folder in the specified projects folder
        if not os.path.isdir(os.path.join(projects_path, 'projects')):
            try:
                os.mkdir(os.path.join(projects_path, 'projects'))
            except OSError as e:
                print('Error creating the "projects" folder: ', e)

        # Moving populse_mia folder to the specified location
        self.copy_directory('populse_mia', os.path.join(mia_path, 'populse_mia'))

        # Updating the checkbox
        self.check_box_mia.setChecked(True)
        QtWidgets.QApplication.processEvents()

        # Moving MRIFileManager folder to the specified location
        self.copy_directory('MRIFileManager', os.path.join(mia_path, 'MRIFileManager'))

        # Updating the checkbox
        self.check_box_mri_conv.setChecked(True)
        QtWidgets.QApplication.processEvents()

        # Adding both mia, MRIFileManager and projects paths to Populse_MIA's config
        config_file = os.path.join(mia_path, 'populse_mia', 'properties', 'config.yml')
        if os.path.isfile(config_file):
            config_dic = self.load_config(config_file)
            config_dic["projects_save_path"] = os.path.join(projects_path, 'projects')
            config_dic["mri_conv_path"] = os.path.join(mia_path, 'MRIFileManager', 'MRIManager.jar')
            config_dic["clinical_mode"] = use_clinical_mode
            self.save_config(config_dic, config_file)

        # Adding mia path to /home/.populse_mia/configuration.yml
        home_config = {'mia_path': os.path.join(mia_path, 'populse_mia')}

        self.save_config(home_config, os.path.join(dot_mia_path, 'configuration.yml'))

        # Updating the checkbox
        self.check_box_config.setChecked(True)
        QtWidgets.QApplication.processEvents()

        # Installing Populse_MIA's modules using pip
        self.install_package('populse-mia')  # Not available yet

        # Upgrading soma-base and capsul: need to be removed when soma-base and capsul last versions will be on PyPi
        self.upgrade_soma_capsul()

        # Updating the checkbox
        self.check_box_pkgs.setChecked(True)
        QtWidgets.QApplication.processEvents()

        # Displaying the result of the installation
        self.last_layout()

    def ok_or_abort(self, button):
        role = self.msg.buttonRole(button)
        if role == QtWidgets.QMessageBox.AcceptRole:  # "OK" has been clicked
            self.folder_exists_flag = False
        else:
            self.folder_exists_flag = True

    @staticmethod
    def upgrade_soma_capsul():
        os.chmod('upgrade_soma_capsul.sh', 0o777)
        subprocess.call('./upgrade_soma_capsul.sh', shell=True)

    @staticmethod
    def copy_directory(src, dest):
        try:
            shutil.copytree(src, dest)
        # Directories are the same
        except shutil.Error as e:
            print('Directory not copied. Error: %s' % e)
        # Any error saying that the directory doesn't exist
        except OSError as e:
            print('Directory not copied. Error: %s' % e)

    @staticmethod
    def load_config(config_file):
        with open(config_file, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    @staticmethod
    def save_config(config_dic, config_file):
        with open(config_file, 'w', encoding='utf8') as configfile:
            yaml.dump(config_dic, configfile, default_flow_style=False, allow_unicode=True)

    @staticmethod
    def install_package(package):
        import importlib
        try:
            importlib.import_module(package)
        except ImportError:
            # TODO: THIS HAS TO BE CHANGED WHEN POPULSE_MIA WILL BE DEPLOYED
            subprocess.call([sys.executable, '-m', 'pip', 'install', '--user', '--extra-index-url',
                             'https://test.pypi.org/simple/', package])
