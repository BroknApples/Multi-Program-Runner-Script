######################### IMPORTS #########################
import sys

from PyQt6.QtWidgets import QApplication, QDialog, QWidget
from PyQt6.QtGui import QIcon

######################### GRAPHICS CODE #########################

######### Window Class #########

class Window(QWidget):
  #Initialize Window
  def __init__(self, width, height, name):
    try:
      super().__init__()

      self.ui_ = UIForm()
      self.ui_.Setup()

      self.width_ = width
      self.height_ = height
      self.name_ = name
    except:
      print("Error Creating QWidget Instance")
      return -1

  def AddWidgets(self):
    app = any

######### UIForm Class #########

class UIForm():
  def __init__(self):
    do = any

  def Setup():
    do_anything = any