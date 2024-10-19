class Stylesheet():
  def __init__(self):
    self.background_color = '#222222'
    self.text_color = 'white'
    self.menu_bar_color = '#272727'
    self.menu_bar_border = '#444444'
    self.menu_color = '#202020'
    self.menu_border = '#444444'
    self.item_color = '#333333'
    self.item_border = '#404040'
    self.item_highlighted = '#505050'
    self.item_pressed = '#474747'
    
    # read in from file and overwrite

class UserSettings():
  def __init__(self):
    # Graphics
    self.WINDOW_MIN_WIDTH = 416
    self.WINDOW_MIN_HEIGHT = 500
    self.WINDOW_MAX_WIDTH = 750
    self.WINDOW_MAX_HEIGHT = 900
    self.SIDEBAR_WIDTH = 75
    
    # read in from ini file and overwrite
    # do stuff here