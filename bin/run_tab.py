"""
run_tab.py - Run tab: execute a simulation and see terminal text output

Authors:
Randy Heiland (heiland@iu.edu)
Dr. Paul Macklin (macklinp@iu.edu)
Rf. Credits.md

"""

import sys
import os
import time
import logging
import tempfile
import shutil
from pathlib import Path
from PyQt5 import QtCore, QtGui
# from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFrame,QApplication,QWidget,QTabWidget,QFormLayout,QLineEdit, QHBoxLayout,QVBoxLayout,QRadioButton,QLabel,QCheckBox,QComboBox,QScrollArea, QPushButton,QPlainTextEdit
from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtCore import QProcess

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class RunModel(QWidget):
    def __init__(self, nanohub_flag, tab_widget, rules_flag, download_menu):
        super().__init__()

        self.nanohub_flag = nanohub_flag
        self.actual_nanohub_flag = False  # reset in pmb.py
        self.tab_widget = tab_widget
        self.rules_flag = rules_flag
        self.download_menu = download_menu

        #-------------------------------------------
        # used with nanoHUB app
        # self.nanohub = True
        # following set in pmb.py
        self.current_dir = ''   
        self.homedir = None
        self.config_file = None
        self.tree = None

        # these get set in pmb.py
        self.config_tab = None
        self.microenv_tab = None
        self.celldef_tab = None
        self.user_params_tab = None
        self.rules_tab = None
        self.vis_tab = None
        self.legend_tab = None
        self.debug_tab = None

        self.output_dir = 'output'

        #-----
        self.sim_output = QWidget()

        self.main_layout = QVBoxLayout()

        self.scroll = QScrollArea()

        self.p = None
        # self.xmin = 0.0
        # self.xmax = 1.0
        # self.ymin = 0.0
        # self.ymax = 1.0

        self.control_w = QWidget()

        self.vbox = QVBoxLayout()

        #------------------
        hbox = QHBoxLayout()

        self.run_button = QPushButton("Run Simulation")
        self.run_button.setStyleSheet("background-color: lightgreen")
        hbox.addWidget(self.run_button)
        self.run_button.clicked.connect(self.run_model_cb)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("background-color: red")
        # self.cancel_button.setStyleSheet("background-color: rgb(250,50,50)")
        hbox.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self.cancel_model_cb)

        # self.cancel_button = QPushButton("Cancel")
        # hbox.addWidget(self.cancel_button)
        # self.new_button.clicked.connect(self.append_more_cb)

        hbox.addWidget(QLabel("Exec:"))
        self.exec_name = QLineEdit()
        if self.nanohub_flag:
            self.exec_name.setText('myproj')
            # self.exec_name.setEnabled(False)
        else:
            # self.exec_name.setText('../myproj')
            self.exec_name.setText('template')
        hbox.addWidget(self.exec_name)

        hbox.addWidget(QLabel("Config:"))
        self.config_xml_name = QLineEdit()
        # self.config_xml_name.setText('mymodel.xml')
        # self.config_xml_name.setText('copy_PhysiCell_settings.xml')
        self.config_xml_name.setText('config.xml')
        hbox.addWidget(self.config_xml_name)

        # self.vbox.addStretch()

        self.vbox.addLayout(hbox)

        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.resize(400,900)  # nope

        self.vbox.addWidget(self.text)

        #==================================================================
        self.control_w.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)

        self.scroll.setWidget(self.control_w) 
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll)

#------------------------------
    def update_xml_from_gui(self):
        self.xml_root = self.tree.getroot()
        logging.debug(f'\n ========================== run_tab.py: update_xml_from_gui(): self.xml_root = {self.xml_root}')
        self.config_tab.xml_root = self.xml_root
        self.microenv_tab.xml_root = self.xml_root
        self.celldef_tab.xml_root = self.xml_root
        self.user_params_tab.xml_root = self.xml_root
        if self.rules_flag:
            self.rules_tab.xml_root = self.xml_root
        # sys.exit(1)

        self.config_tab.fill_xml()
        self.microenv_tab.fill_xml()
        self.celldef_tab.fill_xml()
        self.user_params_tab.fill_xml()
        if self.rules_flag:
            self.rules_tab.fill_xml()

        # self.vis_tab.circle_radius = ET.parse(self.xml_root)
        # tree = ET.parse(xml_file)
        # root = tree.getroot()
        # rwh - warning: assumes "R_circle" name won't change
        # self.vis_tab.mech_voxel_size = float(self.xml_root.find(".//user_parameters//mechanics_voxel_size").text)
        # print("\n\n------------- run_tab(): self.vis_tab.mech_voxel_size = ",self.vis_tab.mech_voxel_size)
        
    def message(self, s):
        self.text.appendPlainText(s)

    def run_model_cb(self):
        logging.debug(f'===========  run_model_cb():  ============')

        if float(self.config_tab.svg_interval.text()) != float(self.config_tab.full_interval.text()):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Warning")
            msg.setInformativeText('The output intervals for SVG and full (in Config Basics) do not match.')
            msg.setWindowTitle("Warning")
            msg.exec_()

        self.run_button.setEnabled(False)

        # if self.nanohub_flag: # copy normal workflow of an app, strange as it is
        if True: # copy normal workflow of an app, strange as it is

                    # make sure we are where we started (app's root dir)
            print(f'\nrun_tab.py------>>>> doing os.chdir to {self.homedir}')
            os.chdir(self.homedir)
            # print(f'\nrun_tab.py------>>>> doing os.chdir to {self.current_dir}')
            # os.chdir(self.current_dir)  # was "homedir"

            # remove any previous data
            # NOTE: this dir name needs to match the <folder>  in /data/<config_file.xml>
            os.system('rm -rf tmpdir*')
            time.sleep(1)
            if os.path.isdir('tmpdir'):
                # something on NFS causing issues...
                tname = tempfile.mkdtemp(suffix='.bak', prefix='tmpdir_', dir='.')
                shutil.move('tmpdir', tname)
            os.makedirs('tmpdir')

            # write the default config file to tmpdir
            # new_config_file = "tmpdir/config.xml"  # use Path; work on Windows?
            tdir = os.path.abspath('tmpdir')
            new_config_file = Path(tdir,"config.xml")

            # write_config_file(new_config_file)  
            # update the .xml config file
            self.update_xml_from_gui()

            # self.config_tab.fill_xml()
            # self.microenv_tab.fill_xml()
            # self.celldef_tab.fill_xml()
            # self.user_params_tab.fill_xml()
            print("\n\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("run_tab.py: ----> writing modified model to ",new_config_file)

            # NOTE! We cannot write/update the original data/*.xml because nanoHUB mounts 
            # that dir (all dirs) as READONLY!!!
            self.tree.write(new_config_file)  # saves modified XML to tmpdir/config.xml 

            # Operate from tmpdir. XML: <folder>,</folder>; temporary output goes here.  May be copied to cache later.
            tdir = os.path.abspath('tmpdir')
            os.chdir(tdir)   # run exec from here on nanoHUB


        if self.vis_tab:
            # self.vis_tab.reset_axes()
            self.vis_tab.reset_model_flag = True
            # self.vis_tab.reset_plot_range()
            # self.vis_tab.init_plot_range(self.config_tab) # heaven help the person who needs to understand this


        if self.p is None:  # No process running.
            self.tab_widget.setTabEnabled(6, True)   # enable (allow to be selected) the Plot tab
            self.tab_widget.setTabEnabled(7, True)   # enable Legend tab
            self.message("Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            # self.p.start("mymodel", ['biobots.xml'])
            exec_str = self.exec_name.text()
            xml_str = self.config_xml_name.text()
            if self.actual_nanohub_flag:
                print(f"run_tab.py: submit --local {exec_str} {xml_str}")
                self.p.start("submit",["--local",exec_str,xml_str])
            else:
                # logging.debug(f'\nrun_tab.py: running: {exec_str}, {xml_str}')
                print(f'\nrun_tab.py: running: {exec_str}, {xml_str}')
                self.p.start(exec_str, [xml_str])

                # print("\n\nrun_tab.py: running: ",exec_str," output/config.xml")
                # self.p.start(exec_str, ["output/config.xml"])
            # self.p = None  # No, don't do this

            # if not self.actual_nanohub_flag:
            #     self.legend_tab.reload_legend()  # rwh: new, not sure about timing - creation vs. display
            self.debug_tab.add_msg("run_tab: calling reload_legend()")
            self.legend_tab.reload_legend()  # rwh: new, not sure about timing - creation vs. display
            self.debug_tab.add_msg("run_tab: back from reload_legend()")
        else:
            # logging.debug(f'self.p is not None???')
            print(f'self.p is not None???')

    def cancel_model_cb(self):
        # logging.debug(f'===========  cancel_model_cb():  ============')
        if self.p:  # process running.
            self.p.kill()
            # self.p.terminate()
            self.run_button.setEnabled(True)

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")
        # self.message(f"Starting in a few secs...")   # only for "Starting"

    def process_finished(self):
        self.message("Process finished.")
        # print("-- process finished.")
        self.vis_tab.first_plot_cb("foo")
        if self.nanohub_flag:
            self.download_menu.setEnabled(True)
        self.p = None
        self.run_button.setEnabled(True)