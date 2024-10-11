######################### IMPORTS ##########  ###############
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
  QMainWindow,
  QWidget,
  QToolBar,
  QStatusBar,
  QMenuBar,
  QLabel,
  QVBoxLayout,
  QCheckBox,
  QPushButton,
  QSlider,
  QLineEdit,
  QProgressBar
)
from PyQt6.QtGui import (
  QIcon,
  QAction
)

from config import *
from helpers import (
  NewFile,
  OpenFile,
  SaveFile,
  SaveAsFile
)

######################### GRAPHICS CODE #########################

######### Window Class #########

class MainWindow(QMainWindow):

  #Initialize Window
  def __init__(self, name, width, height):
    try:
      super(MainWindow, self).__init__()

      self.setMinimumSize(kWindowMinWidth, kWindowMinHeight)
      self.setMaximumSize(kWindowMaxWidth, kWindowMaxHeight)
      self.setBaseSize(width, height)
      self.setWindowTitle(name)

      # Store Width Height and Name
      self.width_ = width
      self.height_ = height
      self.name_ = name

      widget = QLabel("Hello")
      font = widget.font()
      font.setPointSize(30)
      widget.setFont(font)
      widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

      self.setCentralWidget(widget)
    except:
      print("Error Creating the Main Window.\n")
      return
  
  def SetWidgets(self):
    self.__SetMenuBar()
    

    self.__SetStatusBar()
    # toolbar = QToolBar()
    # self.addToolBar(toolbar)

    # button_action = QAction("TOolbar", self)
    # button_action.setStatusTip("This is your button")
    # button_action.triggered.connect(self.MenuBar)
    # button_action.setCheckable(True)
    # toolbar.addAction(button_action)

    # Add widgets to a vertical box
    # layout = QVBoxLayout()

    # widgets = self.GetWidgets()

    # for w in widgets:
    #   layout.addWidget(w())

    # widget = QWidget()
    # widget.setLayout(layout)

  # Setup Menu Bar at top of screen
  def __SetMenuBar(self):
    menu = self.menuBar()

    ########## File ##########
    file_menu = menu.addMenu("&File")

    new_file = QAction("New File", file_menu)
    new_file.setStatusTip("Create and open new file")
    new_file.triggered.connect(NewFile)

    file_menu.addSeparator()

    open_file = QAction("Open File", file_menu)
    open_file.setStatusTip("Open existing file")
    open_file.triggered.connect(OpenFile)
    
    file_menu.addSeparator()

    save_file = QAction("Save", file_menu)
    save_file.setStatusTip("Save current file")
    save_file.triggered.connect(SaveFile)

    file_menu.addSeparator()

    save_as_file = QAction("Save As", file_menu)
    save_as_file.setStatusTip("Save current file as")
    save_as_file.triggered.connect(SaveAsFile)

    file_menu.addAction(new_file)
    file_menu.addAction(open_file)
    file_menu.addAction(save_file)
    file_menu.addAction(save_as_file)
    ########## File ##########

    ########## Edit ##########
    edit_menu = menu.addMenu("&Edit")
    edit_menu.addAction(QAction("Open Button", self))
    ########## Edit ##########

    ########## View ##########
    view_menu = menu.addMenu("&View")
    view_menu.addAction(QAction("Open Button", self))
    ########## View ##########

    ######## Settings ########
    settings_menu = menu.addMenu("&Settings")
    settings_menu.addAction(QAction("Open Button", self))
    ######## Settings ########

    ########## Help ##########
    help_menu = menu.addMenu("&Help")
    help_menu.addAction(QAction("Open Button", self))
    ########## Help ##########

  # Setup status bar that give you tooltips
  def __SetStatusBar(self):
    status_bar = QStatusBar(self)
    self.setStatusBar(status_bar)