######################### IMPORTS #########################
import sys

from PyQt6.QtWidgets import QApplication

from main_window import MainWindow

######################### MAIN CODE #########################

# Create QApplication and do QMainWindow Setup
app = QApplication(sys.argv)
main_window = MainWindow("Test App", 500, 600)
main_window.SetWidgets()

main_window.show()

# Loop Program
sys.exit(app.exec())