######################### IMPORTS #########################
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
  QMainWindow,
  QWidget,
  QStatusBar,
  QDockWidget,
  QVBoxLayout,
  QPushButton
)
from PyQt6.QtGui import (
  QIcon,
  QAction
)

from settings import (
  parseConfigIni,
  UserSettings,
  Stylesheet
)

######################### MAIN_WINDOW CODE #########################

######### Window Class #########

class MainWindow(QMainWindow):

  #Initialize Window
  def __init__(self, name, width, height):
    try:
      super(MainWindow, self).__init__()
    except RuntimeError:
      print("Error creating main window.")
      return
    
    try:
      config = parseConfigIni()
      print(config)
      self.settings = UserSettings(config)
      self.stylesheet = Stylesheet(config)
    except ValueError:
      print("Error setting MainWindow member variables.")
      return
    
    try:
      # Set style
      self.setMinimumSize(self.settings.window_min_width, self.settings.window_min_height)
      self.setMaximumSize(self.settings.window_max_width, self.settings.window_max_height)
      self.setBaseSize(width, height)
      self.setWindowTitle(name)
      self.app_icon = QIcon("bin/gui/logo_16x16.ico")
      self.setWindowIcon(self.app_icon)
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
      self.setStyleSheet("""
        background-color: """ + f'{self.stylesheet.background_color};' + """
        color: """ f'{self.stylesheet.text_color};' + """
      """)

      # Store Width Height and Name
      self.width_m = width
      self.height_m = height
      self.name_m = name

      # Undo and Redo Stacks
      self._undo_stack = []
      self._undo_stack_size = 0
      self._redo_stack = []
      self._redo_stack_size = 0
    except ValueError:
      print("Error Setting Style.")
      return
  

  def SetWidgets(self):
    self.__SetCentralWidget()
    self.__SetMenuBar()
    self.__SetSideBar()
    self.__SetContentBrowser()
    self.__SetStatusBar()

  def __SetCentralWidget(self):
    widget = QWidget()
    self.setCentralWidget(widget)

  def __SetMenuBar(self):
    menu_bar = self.menuBar()

    ########## Style ##########
    menu_bar.setStyleSheet("""
      QMenuBar {
          background-color: """ + f'{self.stylesheet.menu_bar_color};' + """
          border: 1px solid """ + f'{self.stylesheet.menu_bar_border};' + """
          color: """ + f'{self.stylesheet.text_color};' + """
          padding: 3px 3px;
      }

      QMenuBar::item {
          padding: 4px 13px;
          border-radius: 5px;
      }

      QMenuBar::item:selected {
          background-color: """ + f'{self.stylesheet.item_color};' + """
      }

      QMenu {
          background-color: """ + f'{self.stylesheet.item_color};' + """
          border: 1px solid """ + f'{self.stylesheet.item_border};' + """
          border-radius: 5px;
          padding: 2px 2px
      }

      QMenu::item {
          padding: 5px 25px;
      }

      QMenu::item:selected {
          background-color: """ + f'{self.stylesheet.item_highlighted};' + """
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
    undo_button.triggered.connect(self.__Undo)

    redo_button = menu_bar.addAction("&Redo")
    redo_button.triggered.connect(self.__Redo)

    # TODO: set these to update automatically as program runs
    undo_status_tip = "Undo Previous Action: "
    if (self._undo_stack_size > 0):
      undo_status_tip += self._undo_stack[self._undo_stack_size - 1]
    else:
      undo_status_tip += "N/A"
    undo_button.setStatusTip(undo_status_tip)

    redo_status_tip = "Redo Previous Action: "
    if (self._redo_stack_size > 0):
      redo_status_tip += self._redo_stack[self._redo_stack_size - 1]
    else:
      redo_status_tip += "N/A"
    redo_button.setStatusTip(redo_status_tip)
    ##### END Undo & Redo #####

    ##### Minimize & Exit #####
    # minimize_button = menu_bar.addAction("&-")
    # minimize_button.triggered.connect(self.showMinimized)
    # exit_button = menu_bar.addAction("&X")
    # exit_button.triggered.connect(self.close)
    ### END Minimize & Exit ### 
    
  def  __SetSideBar(self):
    self.sidebar = QDockWidget('Tools', self)
    self.sidebar.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
    self.sidebar.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
    self.sidebar.setFixedWidth(self.settings.sidebar_width)

    widget = QWidget()
    vbox = QVBoxLayout(widget)

    ######### Add Item #########
    add_item = QPushButton("+")
    add_item.setStatusTip('Add a new item.')
    vbox.addWidget(add_item)
    ######### Add Item #########

    ######## Remove Item ########
    remove_item = QPushButton("-")
    remove_item.setStatusTip('Remove selected item.')
    vbox.addWidget(remove_item)
    ######## Remove Item ########

    ######## VBOX Styles ########
    vbox.insertStretch(-1, 1) # remove spacing between toolbar options

    ######## VBOX Styles ########

    vbox.parent().setStyleSheet("""
      QWidget {
        background-color: """ + f'{self.stylesheet.menu_color};' + """
        border-right: 1px solid """ + f'{self.stylesheet.menu_border};' + """
        border-left: 1px solid """ + f'{self.stylesheet.menu_border};' + """
        padding: 5px;
        font-size: 15px;
        text-align: center;
      }
                         
      QPushButton {
        background-color: """ + f'{self.stylesheet.menu_color};' + """
        border: 1px solid """ + f'{self.stylesheet.menu_border};' + """
        border-radius: 4px;
      }

      QPushButton:hover {
        background-color: """ + f'{self.stylesheet.item_color};' + """
      }

      QPushButton:pressed {
        background-color: """ + f'{self.stylesheet.item_pressed};' + """
      }
    """)

    self.sidebar.setWidget(vbox.parent())

    self.sidebar.setStyleSheet("""
      QDockWidget::title {
        background-color: """ + f'{self.stylesheet.menu_color};' + """
        border-right: 1px solid """ + f'{self.stylesheet.menu_border};' + """
        border-left: 1px solid """ + f'{self.stylesheet.menu_border};' + """
        text-align: center;
        padding: 5px 0px
      }
    """)

    self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)

  def __SetContentBrowser(self):
    pass

  def __SetStatusBar(self):
    status_bar = QStatusBar(self)
    status_bar.setStyleSheet("""
      QStatusBar {
        background-color: """ + f'{self.stylesheet.menu_color};' + """
        border-top: 1px solid """ + f'{self.stylesheet.menu_border};' + """
      }
    """)
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