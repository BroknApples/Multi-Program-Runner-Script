######################### IMPORTS #########################
import sys

from PyQt6.QtWidgets import QApplication

from graphics import Window

######################### MAIN CODE #########################

# Create QApplication and QWidget Setup
app = QApplication(sys.argv)
window = Window(1920, 1080, "Test App")
window.show()

# Loop Program
sys.exit(app.exec())