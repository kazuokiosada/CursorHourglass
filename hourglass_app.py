import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QSurfaceFormat
from hourglass_widget import HourglassWidget
from menu_handler import MenuHandler

class HourglassApp(QMainWindow):
    def __init__(self):
        # OpenGLのフォーマット設定（ウィンドウ作成前に行う）
        format = QSurfaceFormat()
        format.setVersion(2, 1)
        format.setProfile(QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile)
        format.setDepthBufferSize(24)
        format.setSamples(4)
        format.setAlphaBufferSize(8)
        format.setStencilBufferSize(8)
        format.setSwapBehavior(QSurfaceFormat.SwapBehavior.DoubleBuffer)
        QSurfaceFormat.setDefaultFormat(format)
        
        super().__init__()
        self.initUI()
        
    def initUI(self):
        """UIの初期化"""
        self.setWindowTitle('砂時計')
        self.setGeometry(100, 100, 800, 600)
        
        # メインウィジェットの設定
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 砂時計ウィジェットの作成と設定
        self.hourglass = HourglassWidget()
        self.hourglass.setMinimumSize(400, 400)
        layout.addWidget(self.hourglass)
        
        # メニューハンドラーの設定
        self.menu_handler = MenuHandler(self)
        
        print("Window initialized")

    def mousePressEvent(self, event):
        """マウスクリックイベントの処理"""
        if event.button() == Qt.MouseButton.RightButton:
            self.menu_handler.show_context_menu(event.pos())

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = HourglassApp()
    window.show()
    
    print("Application started")
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 