import sys
import PySide.QtGui as QtGui

class TestUI(QtGui.QWidget):
	def __init__(self):
		super(TestUI, self).__init__()
		self.init_ui()
		
	def init_ui(self):
		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle('Icon')
		



def main():
	app = QtGui.QApplication(sys.argv)
	ui = TestUI()
	ui.show()
	sys.exit(app.exec_())
	
main()

