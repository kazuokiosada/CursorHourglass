from PyQt6.QtWidgets import QMenu, QInputDialog, QColorDialog
from PyQt6.QtGui import QColor

class MenuHandler:
    def __init__(self, parent):
        self.parent = parent
        
    def show_context_menu(self, pos):
        """コンテキストメニューの表示"""
        menu = QMenu(self.parent)
        
        # メニューアイテムの追加
        restart_action = menu.addAction("再計測")
        time_action = menu.addAction("時間変更")
        color_action = menu.addAction("砂の色")
        mode_action = menu.addAction("動作モード切替")
        menu.addSeparator()
        quit_action = menu.addAction("終了")
        
        # アクションの設定
        action = menu.exec(self.parent.mapToGlobal(pos))
        
        if action == restart_action:
            self.restart_measurement()
        elif action == time_action:
            self.change_time()
        elif action == color_action:
            self.change_sand_color()
        elif action == mode_action:
            self.toggle_mode()
        elif action == quit_action:
            self.parent.close()
            
    def restart_measurement(self):
        """計測の再開"""
        self.parent.hourglass.start_measurement()
        
    def change_time(self):
        """計測時間の変更"""
        current_time = self.parent.hourglass.measurement_time // 60
        time, ok = QInputDialog.getInt(
            self.parent, "時間変更",
            "計測時間（分）を入力してください：",
            current_time, 1, 30
        )
        if ok:
            self.parent.hourglass.measurement_time = time * 60
            self.parent.hourglass.start_measurement()
            
    def change_sand_color(self):
        """砂の色の変更"""
        current_color = self.parent.hourglass.sand_color
        color = QColorDialog.getColor(
            QColor.fromRgbF(current_color[0], current_color[1], current_color[2])
        )
        if color.isValid():
            self.parent.hourglass.set_sand_color((
                color.redF(),
                color.greenF(),
                color.blueF()
            ))
            
    def toggle_mode(self):
        """動作モードの切り替え"""
        self.parent.hourglass.continuous_mode = not self.parent.hourglass.continuous_mode 