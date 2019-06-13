import os
import sys
import yaml
import shutil
import tempfile
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore


class MIAInstallWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        self.matlab_path = ""

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

        self.middle_label_text = 'Please select an installation path and a folder to store your future projects and ' \
                                 'set the paths to run Matlab and SPM12.\n\n'

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

        h_box_clinical_mode = QtWidgets.QVBoxLayout()
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

        # Matlab and SPM12 groupboxes

        # Groupbox "Matlab"
        self.groupbox_matlab = QtWidgets.QGroupBox("Matlab")
        self.use_matlab_label = QtWidgets.QLabel("Use Matlab")
        self.use_matlab_checkbox = QtWidgets.QCheckBox('', self)

        matlab_path = self.find_matlab_path()
        self.matlab_label = QtWidgets.QLabel("Matlab path:")
        self.matlab_choice = QtWidgets.QLineEdit(matlab_path)
        self.matlab_browse = QtWidgets.QPushButton("Browse")
        self.matlab_browse.clicked.connect(self.browse_matlab)

        self.matlab_standalone_label = QtWidgets.QLabel("Matlab standalone path:")
        self.matlab_standalone_choice = QtWidgets.QLineEdit()
        self.matlab_standalone_browse = QtWidgets.QPushButton("Browse")
        self.matlab_standalone_browse.clicked.connect(self.browse_matlab_standalone)

        h_box_use_matlab = QtWidgets.QHBoxLayout()
        h_box_use_matlab.addWidget(self.use_matlab_checkbox)
        h_box_use_matlab.addWidget(self.use_matlab_label)
        h_box_use_matlab.addStretch(1)

        h_box_matlab_path = QtWidgets.QHBoxLayout()
        h_box_matlab_path.addWidget(self.matlab_choice)
        h_box_matlab_path.addWidget(self.matlab_browse)

        v_box_matlab_path = QtWidgets.QVBoxLayout()
        v_box_matlab_path.addWidget(self.matlab_label)
        v_box_matlab_path.addLayout(h_box_matlab_path)

        h_box_matlab_standalone_path = QtWidgets.QHBoxLayout()
        h_box_matlab_standalone_path.addWidget(self.matlab_standalone_choice)
        h_box_matlab_standalone_path.addWidget(self.matlab_standalone_browse)

        v_box_matlab_standalone_path = QtWidgets.QVBoxLayout()
        v_box_matlab_standalone_path.addWidget(self.matlab_standalone_label)
        v_box_matlab_standalone_path.addLayout(h_box_matlab_standalone_path)

        v_box_matlab = QtWidgets.QVBoxLayout()
        v_box_matlab.addLayout(h_box_use_matlab)
        v_box_matlab.addLayout(v_box_matlab_path)
        v_box_matlab.addLayout(v_box_matlab_standalone_path)

        self.groupbox_matlab.setLayout(v_box_matlab)

        # Groupbox "SPM"
        self.groupbox_spm = QtWidgets.QGroupBox("SPM")

        self.use_spm_label = QtWidgets.QLabel("Use SPM")
        self.use_spm_checkbox = QtWidgets.QCheckBox('', self)

        self.spm_label =QtWidgets. QLabel("SPM path:")
        self.spm_choice = QtWidgets.QLineEdit()
        self.spm_browse = QtWidgets.QPushButton("Browse")
        self.spm_browse.clicked.connect(self.browse_spm)

        h_box_use_spm = QtWidgets.QHBoxLayout()
        h_box_use_spm.addWidget(self.use_spm_checkbox)
        h_box_use_spm.addWidget(self.use_spm_label)
        h_box_use_spm.addStretch(1)

        h_box_spm_path = QtWidgets.QHBoxLayout()
        h_box_spm_path.addWidget(self.spm_choice)
        h_box_spm_path.addWidget(self.spm_browse)

        v_box_spm_path = QtWidgets.QVBoxLayout()
        v_box_spm_path.addWidget(self.spm_label)
        v_box_spm_path.addLayout(h_box_spm_path)

        self.use_spm_standalone_label = QtWidgets.QLabel("Use SPM standalone")
        self.use_spm_standalone_checkbox = QtWidgets.QCheckBox('', self)

        self.spm_standalone_label = QtWidgets.QLabel("SPM standalone path:")
        self.spm_standalone_choice = QtWidgets.QLineEdit()
        self.spm_standalone_browse = QtWidgets.QPushButton("Browse")
        self.spm_standalone_browse.clicked.connect(self.browse_spm_standalone)

        h_box_use_spm_standalone = QtWidgets.QHBoxLayout()
        h_box_use_spm_standalone.addWidget(self.use_spm_standalone_checkbox)
        h_box_use_spm_standalone.addWidget(self.use_spm_standalone_label)
        h_box_use_spm_standalone.addStretch(1)

        h_box_spm_standalone_path = QtWidgets.QHBoxLayout()
        h_box_spm_standalone_path.addWidget(self.spm_standalone_choice)
        h_box_spm_standalone_path.addWidget(self.spm_standalone_browse)

        v_box_spm_standalone_path = QtWidgets.QVBoxLayout()
        v_box_spm_standalone_path.addWidget(self.spm_standalone_label)
        v_box_spm_standalone_path.addLayout(h_box_spm_standalone_path)

        v_box_spm = QtWidgets.QVBoxLayout()
        v_box_spm.addLayout(h_box_use_spm)
        v_box_spm.addLayout(v_box_spm_path)
        v_box_spm.addLayout(h_box_use_spm_standalone)
        v_box_spm.addLayout(v_box_spm_standalone_path)

        self.groupbox_spm.setLayout(v_box_spm)

        # Final layout
        h_box_mode_paths = QtWidgets.QHBoxLayout()
        h_box_mode_paths.addLayout(h_box_clinical_mode)
        h_box_mode_paths.addWidget(self.groupbox)

        h_box_matlab_spm = QtWidgets.QHBoxLayout()
        h_box_matlab_spm.addWidget(self.groupbox_matlab)
        h_box_matlab_spm.addWidget(self.groupbox_spm)

        self.global_layout = QtWidgets.QVBoxLayout()
        self.global_layout.addLayout(h_box_top_label)
        self.global_layout.addLayout(h_box_middle_label)
        self.global_layout.addStretch(1)
        self.global_layout.addLayout(h_box_mode_paths)
        self.global_layout.addLayout(h_box_matlab_spm)
        self.global_layout.addLayout(h_box_buttons)

        self.setLayout(self.global_layout)
        self.setWindowTitle("Populse_MIA installation")

        # Setting the checkbox values
        if matlab_path == "":
            self.matlab_choice.setDisabled(True)
            self.matlab_standalone_choice.setDisabled(True)
            self.matlab_label.setDisabled(True)
            self.matlab_standalone_label.setDisabled(True)
            self.matlab_browse.setDisabled(True)
            self.matlab_standalone_browse.setDisabled(True)
        else:
            self.install_matlab_api()
            self.use_matlab_checkbox.setChecked(True)
        self.spm_choice.setDisabled(True)
        self.spm_standalone_choice.setDisabled(True)
        self.spm_label.setDisabled(True)
        self.spm_standalone_label.setDisabled(True)
        self.spm_browse.setDisabled(True)
        self.spm_standalone_browse.setDisabled(True)
        self.use_spm_checkbox.setChecked(False)
        self.use_spm_standalone_checkbox.setChecked(False)

        # Signals
        self.use_matlab_checkbox.stateChanged.connect(self.use_matlab_changed)
        self.use_spm_checkbox.stateChanged.connect(self.use_spm_changed)
        self.use_spm_standalone_checkbox.stateChanged.connect(self.use_spm_standalone_changed)

    def find_matlab_path(self):
        return_value = ""
        try:
            out = subprocess.check_output(['matlab', '-nodisplay', '-nosplash', '-nodesktop', '-r',
                                           'disp(matlabroot);exit'])
            out_split = out.split()
            valid_lines = [line for line in out_split if os.path.isdir(line)]
            if len(valid_lines) == 1:
                return_value = os.path.join(valid_lines[0].decode('ascii'), 'bin', 'matlab')

                if os.path.isfile(os.path.join(valid_lines[0].decode('ascii'), 'bin', 'matlab')):
                    self.matlab_path = valid_lines[0].decode('ascii')
                    return_value = os.path.join(valid_lines[0].decode('ascii'), 'bin', 'matlab')
                elif os.path.isfile(os.path.join(valid_lines[0].decode('ascii'), 'bin', 'matlab.exe')):
                    self.matlab_path = valid_lines[0].decode('ascii')
                    return_value = os.path.join(valid_lines[0].decode('ascii'), 'bin', 'matlab.exe')
                else:
                    return_value = ""
        except:
            pass

        return return_value

    def install_matlab_api(self):
        pass
        # TODO: find a way to get the admin rights
        """cur_dir = os.getcwd()
        try:
            if self.matlab_path:
                os.chdir(os.path.join(self.matlab_path, 'extern', 'engines', 'python'))
                subprocess.call([sys.executable, 'setup.py', 'install'])
                os.chdir(cur_dir)
        except:
            os.chdir(cur_dir)"""

    def use_matlab_changed(self):
        """
        Called when the use_matlab checkbox is changed
        """

        if not self.use_matlab_checkbox.isChecked():
            self.matlab_choice.setDisabled(True)
            self.matlab_standalone_choice.setDisabled(True)
            self.spm_choice.setDisabled(True)
            self.spm_standalone_choice.setDisabled(True)
            self.matlab_label.setDisabled(True)
            self.matlab_standalone_label.setDisabled(True)
            self.spm_label.setDisabled(True)
            self.spm_standalone_label.setDisabled(True)
            self.spm_browse.setDisabled(True)
            self.spm_standalone_browse.setDisabled(True)
            self.matlab_browse.setDisabled(True)
            self.matlab_standalone_browse.setDisabled(True)
            self.use_spm_checkbox.setChecked(False)
            self.use_spm_standalone_checkbox.setChecked(False)
        else:
            self.matlab_choice.setDisabled(False)
            self.matlab_standalone_choice.setDisabled(False)
            self.matlab_label.setDisabled(False)
            self.matlab_standalone_label.setDisabled(False)
            self.matlab_browse.setDisabled(False)
            self.matlab_standalone_browse.setDisabled(False)

    def use_spm_standalone_changed(self):
        """
        Called when the use_spm_standalone checkbox is changed
        """

        if not self.use_spm_standalone_checkbox.isChecked():
            self.spm_standalone_choice.setDisabled(True)
            self.spm_standalone_label.setDisabled(True)
            self.spm_standalone_browse.setDisabled(True)
        else:
            self.spm_standalone_choice.setDisabled(False)
            self.spm_standalone_label.setDisabled(False)
            self.spm_standalone_browse.setDisabled(False)
            self.spm_choice.setDisabled(True)
            self.spm_label.setDisabled(True)
            self.spm_browse.setDisabled(True)
            self.use_spm_checkbox.setChecked(False)

    def use_spm_changed(self):
        """
        Called when the use_spm checkbox is changed
        """

        if not self.use_spm_checkbox.isChecked():
            self.spm_choice.setDisabled(True)
            self.spm_label.setDisabled(True)
            self.spm_browse.setDisabled(True)
        else:
            self.spm_choice.setDisabled(False)
            self.spm_label.setDisabled(False)
            self.spm_browse.setDisabled(False)
            self.spm_standalone_choice.setDisabled(True)
            self.spm_standalone_label.setDisabled(True)
            self.spm_standalone_browse.setDisabled(True)
            self.use_spm_standalone_checkbox.setChecked(False)

    def browse_matlab(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose Matlab executable file')[0]
        if fname:
            self.matlab_choice.setText(fname)

    def browse_matlab_standalone(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose MCR directory')
        if fname:
            self.matlab_standalone_choice.setText(fname)

    def browse_spm(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose SPM directory')
        if fname:
            self.spm_choice.setText(fname)

    def browse_spm_standalone(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Choose SPM standalone directory')
        if fname:
            self.spm_standalone_choice.setText(fname)

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

        mia_command_label_text = "To launch Populse_MIA, execute one of these command lines depending on your Python " \
                                 "setup:\n\npython3 -m populse_mia\n\npython -m populse_mia"
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
            use_clinical_mode = True
            self.operating_mode = "clinical"
        else:
            use_clinical_mode = False
            self.operating_mode = "research"

        if self.use_matlab_checkbox.isChecked():
            use_matlab = True
            matlab = self.matlab_choice.text()
            matlab_standalone = self.matlab_standalone_choice.text()
        else:
            use_matlab = False
            matlab = ""
            matlab_standalone = ""

        if self.use_spm_checkbox.isChecked():
            use_spm = True
            spm = self.spm_choice.text()
        else:
            use_spm = False
            spm = ""

        if self.use_spm_standalone_checkbox.isChecked():
            use_spm_standalone = True
            spm_standalone = self.spm_standalone_choice.text()
        else:
            use_spm_standalone = False
            spm_standalone = ""

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
            config_dic["use_matlab"] = use_matlab
            config_dic["matlab"] = matlab
            config_dic["matlab_standalone"] = matlab_standalone
            config_dic["use_spm"] = use_spm
            config_dic["spm"] = spm
            config_dic["use_spm_standalone"] = use_spm_standalone
            config_dic["spm_standalone"] = spm_standalone
            self.save_config(config_dic, config_file)

        # Adding mia path to /home/.populse_mia/configuration.yml
        home_config = {'mia_path': os.path.join(mia_path, 'populse_mia')}

        self.save_config(home_config, os.path.join(dot_mia_path, 'configuration.yml'))

        # Updating the checkbox
        self.check_box_config.setChecked(True)
        QtWidgets.QApplication.processEvents()

        # Installing Populse_MIA's modules using pip
        self.install_package('populse-mia')

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

    def upgrade_soma_capsul(self):
        temp_dir = tempfile.mkdtemp()
        cwd = os.getcwd()
        try:
            # Updating capsul
            self.uninstall_package('capsul')
            subprocess.call(['git', 'clone', 'https://github.com/populse/capsul.git', os.path.join(temp_dir, 'capsul')])
            os.chdir(os.path.join(temp_dir, 'capsul'))
            subprocess.call([sys.executable, 'setup.py', 'install', '--user', '--force', '--prefix='])
        except:
            print('\n\nProblem while upgrading capsul...')

        try:
            # Updating soma-base
            self.uninstall_package('soma-base')
            subprocess.call(['git', 'clone', 'https://github.com/populse/soma-base.git', os.path.join(temp_dir, 'soma-base')])
            os.chdir(os.path.join(temp_dir, 'soma-base'))
            subprocess.call([sys.executable, 'setup.py', 'install', '--user', '--force', '--prefix='])
        except:
            print('\n\nProblem while upgrading soma-base...')

            '''if not os.name == 'nt':  # if not on windows
                self.uninstall_package('capsul')
                os.chmod('upgrade_capsul.sh', 0o777)
                subprocess.call('./upgrade_capsul.sh', shell=True)
    
                self.uninstall_package('soma-base')
                os.chmod('upgrade_soma.sh', 0o777)
                subprocess.call('./upgrade_soma.sh', shell=True)'''

        os.chdir(cwd)
        shutil.rmtree(temp_dir, ignore_errors=True)

    @staticmethod
    def copy_directory(src, dest):
        file_directory = os.path.dirname(os.path.realpath(__file__))
        src_path = os.path.join(file_directory, src)
        try:
            shutil.copytree(src_path, dest)
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
        subprocess.call([sys.executable, '-m', 'pip', 'install', '--user', '--upgrade', package])
        # subprocess.call([sys.executable, '-m', 'pip', 'install', '--user', '--extra-index-url',
        #                  'https://test.pypi.org/simple/', package])

    @staticmethod
    def uninstall_package(package):
        try:
            subprocess.call([sys.executable, '-m', 'pip', 'uninstall', '--yes', package])
        except:
            subprocess.call(['pip3', 'uninstall', '--yes', package])
