class Stylesheet():
  def __init__(self):
    self.bg_color = '#222222'
    self.text_color = 'white'
    self.menu_color = '#252525'
    self.menu_border = '#555555'
    self.menu_highlighted = '#333333'
    
    # read in from file and overwrite

class UserSettings():
  def __init__(self):
    #Graphics
    self.WINDOW_MIN_WIDTH = 416
    self.WINDOW_MIN_HEIGHT = 500
    self.WINDOW_MAX_WIDTH = 750
    self.WINDOW_MAX_HEIGHT = 900
    self.SIDEBAR_WIDTH = 75
    
    self._stylesheet = Stylesheet()
    
    # read in from ini file and overwrite
    # do stuff here