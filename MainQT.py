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
from LiabilityClean import combine_liability_and_orders
import datetime
from GetDataFromServer import get_data_for_ratings

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
        font = QtGui.QFont()
        font.setPointSize(15)
        self.cal = QtGui.QCalendarWidget(self.centralwidget)
        self.cal.setGridVisible(True)
        self.cal.move(65, 128)
        self.cal.setFirstDayOfWeek(QtCore.Qt.Monday)
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
        self.cal.setSelectedDate(QtCore.QDate.currentDate())
        main_window.setWindowTitle(
            QtGui.QApplication.translate("main_window", "OptiEdit 2.2.0", None, QtGui.QApplication.UnicodeUTF8))
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
        if datetime.datetime(self.cal.selectedDate().year(), self.cal.selectedDate().month(),
                             self.cal.selectedDate().day()).isoweekday() < 5 and network % 2 == 0:
            daypartList = ['Daytime', 'Prime Access', 'Prime 2', 'Early Fringe']
        elif datetime.datetime(self.cal.selectedDate().year(), self.cal.selectedDate().month(),
                               self.cal.selectedDate().day()).isoweekday() < 5:
            daypartList = ['Morning', 'Daytime', 'Early Fringe', 'Prime Access', 'Prime 2']
        elif datetime.datetime(self.cal.selectedDate().year(), self.cal.selectedDate().month(),
                               self.cal.selectedDate().day()).isoweekday() >= 5 and network % 2 == 0:
            daypartList = ['Weekend', 'Prime 2']
        else:
            daypartList = ['Weekend Morning', 'Weekend Day', 'Prime Access', 'Prime 2']

        total_returned = 0
        dateString = str(self.cal.selectedDate().year()) + "-" + str(self.cal.selectedDate().month()) + "-" + str(
            self.cal.selectedDate().day())

        liability_file = combine_liability_and_orders(network)
        ratings_file = get_data_for_ratings(network, dateString)



        for dayparts in daypartList:
            number_of_returned = start_calculation(dayparts, config['DEFAULT']['RATINGS_PATH'],
                                                   config['DEFAULT']['SPOTS_PATH'],
                                                   times, datetime.datetime(self.cal.selectedDate().year(),
                                                                            self.cal.selectedDate().month(),
                                                                            self.cal.selectedDate().day()).isoweekday(),
                                                   network, breaks, liability_file, dateString, ratings_file)
            total_returned += number_of_returned
            completed += (100 // len(daypartList))
            self.pbar.setValue(completed)

        self.pbar.setHidden(True)
        self.cal.setHidden(True)
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
            loginLayout.addWidget(self.labels[i - 7], i - 7, 0)
            loginLayout.addWidget(self.boxes[i - 7], i - 7, 1)
            loginLayout.addWidget(self.breaks[i - 7], i - 7, 2)

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
