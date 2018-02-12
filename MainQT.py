# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\143740\Desktop\OptiEdit Files\MainWindow.ui'
#
# Created: Tue May 24 09:00:35 2016
# by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from StartCalculation import start_calculation
import configparser
import os.path

config = configparser.ConfigParser()
if os.path.isfile('user.ini'):
    config.read('user.ini')
    times = [int(config['DEFAULT']['DEFAULT_POTENTIAL'])] * 17

if os.path.isfile('user.ini'):
    config.read('user.ini')
    breaks = [int(config['DEFAULT']['DEFAULT_BREAKS'])] * 17


# noinspection PyCallByClass
class Ui_main_window(object):
    def setupUi(self, main_window):
        if os.path.isfile('user.ini'):
            config.read('user.ini')
        else:
            config['DEFAULT'] = {'NETWORK': 'Travel Channel',
                                 'DEFAULT_POTENTIAL': 780,
                                 'RATINGS_PATH': r'F:\\Traffic Logs\\Travel\\OptiEdit\\Travel Ratings\\',
                                 'SPOTS_PATH': r'F:\\Traffic Logs\\Travel\\OptiEdit\\Travel Spots\\',
                                 'DEFAULT_BREAKS': 5}
            with open('user.ini', 'w') as configfile:
                config.write(configfile)

        global times
        times = [int(config['DEFAULT']['DEFAULT_POTENTIAL'])] * 18

        network_list = ['Food Network', 'HGTV', 'Travel Channel']
        starting_index = network_list.index(config['DEFAULT']['NETWORK'])
        main_window.setObjectName("main_window")
        main_window.resize(400, 400)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(130, 116, 125))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(130, 116, 125))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(130, 116, 125))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(130, 116, 125))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        main_window.setPalette(palette)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main_window.setWindowIcon(icon)
        main_window.setAutoFillBackground(True)
        main_window.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralwidget = QtGui.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 300, 400, 80))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 153, 162))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 153, 162))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 153, 162))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(144, 153, 162))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.frame.setPalette(palette)
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtGui.QFrame.WinPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setLineWidth(6)
        self.frame.setObjectName("frame")
        self.needlessButton = QtGui.QPushButton(self.frame)
        self.needlessButton.setGeometry(QtCore.QRect(10, 10, 61, 61))
        self.needlessButton.setIcon(icon)
        self.needlessButton.setIconSize(QtCore.QSize(61, 61))
        self.needlessButton.setObjectName("needlessButton")
        self.customizeButton = QtGui.QPushButton(self.frame)
        self.customizeButton.setGeometry(QtCore.QRect(140, 20, 121, 41))
        self.customizeButton.clicked.connect(self.customize)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.customizeButton.setFont(font)
        self.customizeButton.setObjectName("customizeButton")
        self.optimizeButton = QtGui.QPushButton(self.frame)
        self.optimizeButton.setGeometry(QtCore.QRect(270, 20, 121, 41))
        self.optimizeButton.clicked.connect(self.optimize)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.optimizeButton.setFont(font)
        self.optimizeButton.setObjectName("optimizeButton")
        self.networkSelectCombo = QtGui.QComboBox(self.centralwidget)
        self.networkSelectCombo.setGeometry(QtCore.QRect(100, 60, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setStrikeOut(False)
        self.networkSelectCombo.setFont(font)
        self.networkSelectCombo.setObjectName("networkSelectCombo")
        self.networkSelectCombo.addItem("")
        self.networkSelectCombo.addItem("")
        self.networkSelectCombo.addItem("")
        self.networkSelectCombo.setCurrentIndex(starting_index)
        self.daySelectCombo = QtGui.QComboBox(self.centralwidget)
        self.daySelectCombo.setGeometry(QtCore.QRect(100, 170, 211, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(113, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(113, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(113, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.daySelectCombo.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.daySelectCombo.setFont(font)
        self.daySelectCombo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.daySelectCombo.setObjectName("daySelectCombo")
        self.daySelectCombo.addItem("")
        self.daySelectCombo.addItem("")
        self.daySelectCombo.addItem("")
        self.daySelectCombo.addItem("")
        self.daySelectCombo.addItem("")
        self.daySelectCombo.addItem("")
        self.daySelectCombo.addItem("")
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        main_window.setMenuBar(self.menubar)
        self.actionSettings = QtGui.QAction(main_window)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSettings.triggered.connect(self.show_settings)
        self.actionExit = QtGui.QAction(main_window)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.pbar = QtGui.QProgressBar(main_window)
        self.pbar.setGeometry(135, 145, 200, 25)
        self.pbar.setHidden(True)

        self.label = QtGui.QLabel("<font color=black size=20>Hello World</font>", main_window)
        self.label.setGeometry(55, 145, 300, 35)
        self.label.setHidden(True)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    # noinspection PyTypeChecker
    def retranslateUi(self, main_window):
        main_window.setWindowTitle(
            QtGui.QApplication.translate("main_window", "OptiEdit 2.1.6", None, QtGui.QApplication.UnicodeUTF8))
        self.customizeButton.setText(
            QtGui.QApplication.translate("main_window", "Customize", None, QtGui.QApplication.UnicodeUTF8))
        self.optimizeButton.setText(
            QtGui.QApplication.translate("main_window", "Optimize", None, QtGui.QApplication.UnicodeUTF8))
        self.networkSelectCombo.setItemText(0, QtGui.QApplication.translate("main_window", "Food Network", None,
                                                                            QtGui.QApplication.UnicodeUTF8))
        self.networkSelectCombo.setItemText(1, QtGui.QApplication.translate("main_window", "HGTV", None,
                                                                            QtGui.QApplication.UnicodeUTF8))
        self.networkSelectCombo.setItemText(2, QtGui.QApplication.translate("main_window", "Travel Channel", None,
                                                                            QtGui.QApplication.UnicodeUTF8))
        self.daySelectCombo.setItemText(0, QtGui.QApplication.translate("main_window", "Monday", None,
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.daySelectCombo.setItemText(1, QtGui.QApplication.translate("main_window", "Tuesday", None,
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.daySelectCombo.setItemText(2, QtGui.QApplication.translate("main_window", "Wednesday", None,
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.daySelectCombo.setItemText(3, QtGui.QApplication.translate("main_window", "Thursday", None,
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.daySelectCombo.setItemText(4, QtGui.QApplication.translate("main_window", "Friday", None,
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.daySelectCombo.setItemText(5, QtGui.QApplication.translate("main_window", "Saturday", None,
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.daySelectCombo.setItemText(6, QtGui.QApplication.translate("main_window", "Sunday", None,
                                                                        QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(
            QtGui.QApplication.translate("main_window", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(
            QtGui.QApplication.translate("main_window", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(
            QtGui.QApplication.translate("main_window", "Exit", None, QtGui.QApplication.UnicodeUTF8))


    def optimize(self):

        if os.path.isfile('user.ini'):
            config.read('user.ini')

        network = self.networkSelectCombo.currentIndex()

        completed = 0
        self.pbar.setHidden(False)
        self.pbar.setValue(0)
        if self.daySelectCombo.currentIndex() < 5 and network % 2 == 0:
            daypartList = ['Daytime', 'Prime Access', 'Prime 2', 'Early Fringe']
        elif self.daySelectCombo.currentIndex() < 5:
            daypartList = ['Morning', 'Daytime', 'Early Fringe', 'Prime Access', 'Prime 2']
        elif self.daySelectCombo.currentIndex() >= 5 and network % 2 == 0:
            daypartList = ['Weekend', 'Prime 2']
        else:
            daypartList = ['Weekend Morning', 'Weekend Day', 'Prime Access', 'Prime 2']

        total_returned = 0

        for dayparts in daypartList:
            number_of_returned = start_calculation(dayparts, config['DEFAULT']['RATINGS_PATH'],
                                                   config['DEFAULT']['SPOTS_PATH'],
                                                   times,
                                                   self.daySelectCombo.currentText(), network, breaks)
            total_returned += number_of_returned
            completed += (100 // len(daypartList))
            self.pbar.setValue(completed)

        self.pbar.setHidden(True)
        self.daySelectCombo.setHidden(True)
        self.networkSelectCombo.setHidden(True)

        font = QtGui.QFont()
        font.setPointSize(15)

        self.label.setText('All done with {} unplaced spots'.format(total_returned))
        self.label.setFont(font)
        self.label.setHidden(False)

    def show_settings(self):
        w2 = LoginDialog()
        if w2.exec_():
            pass

    def customize(self):
        w3 = CustomizeDialog()
        if w3.exec_():
            pass


class CustomizeDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(CustomizeDialog, self).__init__(parent)

        self.setWindowTitle('OptiEdit')
        loginLayout = QtGui.QGridLayout()


        self.boxes = []
        self.breaks = []
        self.labels = []

        for x in range(0, 17):
            self.boxes.append(QtGui.QLineEdit())
            self.boxes[x].setText(config['DEFAULT']['DEFAULT_POTENTIAL'])
            self.boxes[x].setFixedWidth(50)
            self.breaks.append(QtGui.QLineEdit())
            self.breaks[x].setText(config['DEFAULT']['DEFAULT_BREAKS'])
            self.breaks[x].setFixedWidth(50)
            self.labels.append(QtGui.QLabel(str(x + 7)))
            self.labels[x].setFixedWidth(15)

        for i in range(7, 24):
            loginLayout.addWidget(self.labels[i - 7], i-7, 0)
            loginLayout.addWidget(self.boxes[i - 7], i-7, 1)
            loginLayout.addWidget(self.breaks[i - 7], i-7, 2)

        button = QtGui.QPushButton("OK")
        loginLayout.addWidget(button, 18, 2)

        button.clicked.connect(self.check)

        self.setLayout(loginLayout)
        self.show()

    def check(self):
        global times
        global breaks
        times = [int(self.boxes[x].text()) for x in range(len(self.boxes))]
        breaks = [int(self.breaks[x].text()) for x in range(len(self.breaks))]
        self.accept()


class LoginDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        self.setWindowTitle("OptiEdit")
        self.cb = QtGui.QComboBox()
        self.cb.addItem('Food Network', 1)
        self.cb.addItem('HGTV', 2)
        self.cb.addItem('Travel Channel', 3)

        self.password = QtGui.QLineEdit()
        loginLayout = QtGui.QFormLayout()
        loginLayout.addRow("Network", self.cb)
        loginLayout.addRow("Default Potential", self.password)

        self.buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.check)
        self.buttons.rejected.connect(self.reject)

        layout = QtGui.QVBoxLayout()
        layout.addLayout(loginLayout)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def check(self):

        global times
        times = [self.password.text()] * 18

        if self.cb.currentText() == 'Food Network':
            default_ratings_path = 'F:\\Traffic Logs\\FOOD LOGS\\OptiEdit\\Food Ratings\\'
            default_spots_path = 'F:\\Traffic Logs\\FOOD LOGS\\OptiEdit\\Food Spots\\'
            default_breaks = 5
        elif self.cb.currentText() == 'HGTV':
            default_ratings_path = 'F:\\Traffic Logs\\HGTV\\OptiEdit\\HGTV Ratings\\'
            default_spots_path = 'F:\\Traffic Logs\\HGTV\\OptiEdit\\HGTV Spots\\'
            default_breaks = 6
        else:
            default_ratings_path = 'F:\\Traffic Logs\\Travel\\OptiEdit\\Travel Ratings\\'
            default_spots_path = 'F:\\Traffic Logs\\Travel\\OptiEdit\\Travel Spots\\'
            default_breaks = 5

        self.config = configparser.ConfigParser()
        self.config['DEFAULT'] = {'NETWORK': self.cb.currentText(),
                                  'DEFAULT_POTENTIAL': int(self.password.text()),
                                  'RATINGS_PATH': default_ratings_path,
                                  'SPOTS_PATH': default_spots_path,
                                  'DEFAULT_BREAKS': default_breaks}
        with open('user.ini', 'w') as configfile:
            self.config.write(configfile)
        self.accept()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    main_window = QtGui.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())

