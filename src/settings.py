def parseConfigIni() -> dict[str, str]:
  CONFIG_PATH = 'bin/config.ini'
  with open(CONFIG_PATH, 'r') as readfile:
    text = readfile.read()

  config = {}
  key = value = ''
  equal_sign: bool = False
  comment: bool = False
  
  for ch in text:
    if (ch == '/' or comment): # current section of text is a comment
      if (ch == '\n'):
        comment = False
        continue
      else:
        comment = True
        continue
    elif (ch == ';'): # text section end
      config[key] = value
      key = value = ''
      equal_sign = False
      continue
    elif (ch == '='): # anything past this is for the 'value' var
      equal_sign = True
    elif (ch == ' ' or ch == '\t' or ch == '\n'): # skip spaces, tabs, and new lines
      continue
    elif (not equal_sign): # data for 'key' var
      key += ch
    else: # equal_sign = True | data for 'value' var
      value += ch
  
  return config

class UserSettings():
  def __init__(self, config: dict[str, str]):
    ########### Graphics ###########
    # defaults:
    self.window_min_width  = 416
    self.window_min_height = 500
    self.window_max_width  = 750
    self.window_max_height = 900
    self.sidebar_width     = 75

    # overrides:
    self.window_min_width  = int(config['window_min_width'])
    self.window_min_height = int(config['window_min_height'])
    self.window_max_width  = int(config['window_max_width'])
    self.window_max_height = int(config['window_max_height'])
    self.sidebar_width     = int(config['sidebar_width'])
    ########### Graphics ###########

class Stylesheet():
  def __init__(self, config: dict[str, str]):
    # defaults:
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

    # override
    self.background_color = config['background_color']
    self.text_color       = config['text_color']
    self.menu_bar_color   = config['menu_bar_color']
    self.menu_bar_border  = config['menu_bar_border']
    self.menu_color       = config['menu_color']
    self.menu_border      = config['menu_border']
    self.item_color       = config['item_color']
    self.item_border      = config['item_border']
    self.item_highlighted = config['item_highlighted']
    self.item_pressed     = config['item_pressed']