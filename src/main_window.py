######################### IMPORTS #########################
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
  QMainWindow,
  QWidget,
  QToolBar,
  QStatusBar,
  QMenu,
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

# STYLE SHEET EX:
#self.setStyleSheet("background-color: #DC06C4; color: white;")

######################### MAIN_WINDOW CODE #########################

######### Window Class #########

class MainWindow(QMainWindow):

  #Initialize Window
  def __init__(self, name, width, height):
    try:
      super(MainWindow, self).__init__()

      # Set style
      self.setMinimumSize(kWindowMinWidth, kWindowMinHeight)
      self.setMaximumSize(kWindowMaxWidth, kWindowMaxHeight)
      self.setBaseSize(width, height)
      self.setWindowTitle(name)
      self.app_icon = QIcon("bin/gui/logo_16x16.ico")
      self.setWindowIcon(self.app_icon)
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
      self.setStyleSheet("""
            background-color: #222222; /* Dark gray background */
            color: white;" /* White text color */
            """)

      # Store Width Height and Name
      self.width_ = width
      self.height_ = height
      self.name_ = name

      # Undo and Redo Stacks
      self.undo_stack = []
      self.undo_stack_size = 0
      self.redo_stack = []
      self.redo_stack_size = 0
    except:
      print("Error Creating the Main Window.\n")
      return
  

  def SetWidgets(self):
    self.__SetMenuBar()
    # add more here
    self.__SetStatusBar()

  # Setup Menu Bar at top of screen
  def __SetMenuBar(self):
    menu_bar = self.menuBar()

    ########## Style ##########
    menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #252525; /* Dark gray background */
                color: white; /* White text color */
                border: 1px solid #2A2A2A;
                padding: 3px 3px;
            }

            QMenuBar::item {
                padding: 4px 13px;
                border-radius: 5px;
            }

            QMenuBar::item:selected {
                background-color: #444444; /* Light gray background on hover */
            }

            QMenu {
                background-color: #333333; /* Dark gray background for the menu */
                border: 1px solid #555555;
                border-radius: 5px;
            }

            QMenu::item {
                border: 1px solid #373737;
                border-radius: 5px;
                padding: 5px 25px;
            }

            QMenu::item:selected {
                background-color: #444444; /* Light gray background on hover */
                border-radius: 5px;
            }
        """)
    
    ######## END Style ########

    ########## File ##########
    file_menu = menu_bar.addMenu("&File")

    new_file = QAction("New File", file_menu)
    new_file.setStatusTip("Create and open new file")
    new_file.triggered.connect(self.__NewFile)

    file_menu.addSeparator()

    open_file = QAction("Open File", file_menu)
    open_file.setStatusTip("Open existing file")
    open_file.triggered.connect(self.__OpenFile)
    
    file_menu.addSeparator()

    save_file = QAction("Save", file_menu)
    save_file.setStatusTip("Save current file")
    save_file.triggered.connect(self.__SaveFile)

    file_menu.addSeparator()

    save_as_file = QAction("Save As", file_menu)
    save_as_file.setStatusTip("Save current file as")
    save_as_file.triggered.connect(self.__SaveAsFile)

    file_actions = [
      new_file,
      open_file,
      save_file,
      save_as_file
    ]
    file_menu.addActions(file_actions)

    ######## END File ########

    ######## Settings ########
    settings_menu = menu_bar.addMenu("&Settings")

    open_settings_page = QAction("Settings", settings_menu)
    open_settings_page.setStatusTip("Open default page in the settings menu")
    open_settings_page.triggered.connect(self.__OpenSettingsPage)

    settings_menu.addSeparator()

    open_keyboard_shortcuts_page = QAction("Edit Keyboard Shortcuts", settings_menu)
    open_keyboard_shortcuts_page.setStatusTip("Open keyboard shortcuts page in the settings menu")
    open_keyboard_shortcuts_page.triggered.connect(self.__OpenKeyboardShortcutsPage)

    settings_menu.addSeparator()

    open_theme_page = QAction("Edit Theme", settings_menu)
    open_theme_page.setStatusTip("Open theme page in the settings menu")
    open_theme_page.triggered.connect(self.__OpenThemePage)
    
    settings_actions = [
      open_settings_page,
      open_keyboard_shortcuts_page,
      open_theme_page
    ]
    settings_menu.addActions(settings_actions)

    ###### END Settings ######

    ########## Help ##########
    help_menu = menu_bar.addMenu("&Help")

    show_keyboard_shortcut_reference = QAction("Keyboard Shortcut Reference", help_menu)
    show_keyboard_shortcut_reference.setStatusTip("Open a page containing all keyboard shortcuts")
    show_keyboard_shortcut_reference.triggered.connect(self.__ShowKeyboardShortcutsReference)

    file_menu.addSeparator()

    show_documentation = QAction("Show Documentation", help_menu)
    show_documentation.setStatusTip("Open a page containing all documentation")
    show_documentation.triggered.connect(self.__ShowDocumentation)
    
    file_menu.addSeparator()

    show_about = QAction("Show About", help_menu)
    show_about.setStatusTip("Open the about page")
    show_about.triggered.connect(self.__ShowAbout)

    file_menu.addSeparator()

    show_license = QAction("Show License", help_menu)
    show_license.setStatusTip("Open a page containing the license")
    show_license.triggered.connect(self.__ShowLicense)

    help_actions = [
      show_keyboard_shortcut_reference,
      show_documentation,
      show_about,
      show_license
    ]
    help_menu.addActions(help_actions)
    ######## END Help ########

    ####### Undo & Redo #######
    undo_button = menu_bar.addAction("&Undo")
    undo_status_tip = "Undo Previous Action: "
    if len(self.undo_stack) > 0:
      undo_status_tip += self.undo_stack[-1]
    else:
      undo_status_tip += "N/A"
    undo_button.setStatusTip(undo_status_tip)
    undo_button.triggered.connect(self.__Undo)

    redo_button = menu_bar.addAction("&Redo")
    redo_status_tip = "Redo Previous Action: "
    if len(self.undo_stack) > 0:
      redo_status_tip += self.undo_stack[-1]
    else:
      redo_status_tip += "N/A"
    redo_button.setStatusTip(redo_status_tip)
    redo_button.triggered.connect(self.__Redo)
    ##### END Undo & Redo #####

    ##### Minimize & Exit #####
    # minimize_button = menu_bar.addAction("&-")
    # minimize_button.triggered.connect(self.showMinimized)
    # exit_button = menu_bar.addAction("&X")
    # exit_button.triggered.connect(self.close)
    ### END Minimize & Exit ###
    

  # Setup status bar that give you tooltips
  def __SetStatusBar(self):
    status_bar = QStatusBar(self)
    self.setStatusBar(status_bar)




  ############################################################################
  ############################# Helper Functions #############################
  ############################################################################
  ############# Menu Bar - File #############
  def __NewFile(button_state):
    print("Creating a new file")

  def __OpenFile(button_state):
    print("Opening a file")

  def __SaveFile(button_state):
    print("Saving a file")

  def __SaveAsFile(button_state):
    print("Saving a file as")

  ########### Menu Bar - Settings ###########

  def __OpenSettingsPage(button_state):
    print("Opening the settings page")

  def __OpenKeyboardShortcutsPage(button_state):
    print("Opening keyboard shortcuts page in settings")

  def __OpenThemePage(button_state):
    print("Opening theme page in settings")


  ############# Menu Bar - Help #############
  def __ShowKeyboardShortcutsReference(button_state):
    print("Showing all keyboard shortcuts")

  def __ShowDocumentation(button_state):
    print("Showing documentation")


  def __ShowAbout(button_state):
    print("Showing about page")


  def __ShowLicense(button_state):
    print("Showing license")

  ######### Menu Bar - Undo & Redo #########
  def __Undo(button_state):
    print("Undoing action")

  def __Redo(button_state):
    print("Redoing action")