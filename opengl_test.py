import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtGui import QSurfaceFormat
from OpenGL.GL import *

class TestGLWidget(QOpenGLWidget):
    def initializeGL(self):
        print("OpenGL Version:", glGetString(GL_VERSION))
        glClearColor(0.2, 0.2, 0.2, 1.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        format = QSurfaceFormat()
        format.setVersion(2, 1)
        QSurfaceFormat.setDefaultFormat(format)
        
        self.glWidget = TestGLWidget()
        self.setCentralWidget(self.glWidget)
        self.setGeometry(100, 100, 400, 400)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec()) 