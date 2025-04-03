import OpenGL
OpenGL.ERROR_CHECKING = True
OpenGL.FORWARD_COMPATIBLE_ONLY = False

from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt, QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

class HourglassWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 基本的なパラメータ
        self.sand_color = (0.8, 0.6, 0.2)  # 砂の色を黄土色に変更
        self.frame_color = (0.7, 0.5, 0.7)  # 枠の色
        
        # 砂のパラメータ
        self.sand_particles = []  # 砂粒子の位置を格納
        self.sand_flow_rate = 100  # 1秒あたりの落下する砂粒子の数
        self.total_sand = 1000  # 総砂粒子数
        self.sand_in_upper = self.total_sand  # 上部の砂の量
        
        # タイマーの設定
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_sand)
        self.timer.start(16)  # 約60FPS
        
        print("HourglassWidget initialized")

    def initializeGL(self):
        """OpenGLの初期化"""
        print("initializeGL called")
        try:
            glClearColor(0.2, 0.2, 0.2, 1.0)
            glEnable(GL_DEPTH_TEST)
            print("OpenGL initialization successful")
        except Exception as e:
            print(f"Error in initializeGL: {e}")

    def resizeGL(self, width, height):
        """リサイズ時の処理"""
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        """描画処理"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # カメラの位置を調整
        glTranslatef(0.0, 0.0, -4.0)
        glRotatef(15, 1.0, 0.0, 0.0)  # 少し上から見下ろす角度
        
        # 砂時計を描画
        self.draw_hourglass()
        self.draw_sand()

    def draw_hourglass(self):
        """砂時計の基本形状を描画"""
        self.draw_frame()  # トーラスのみ表示するように修正
        self.draw_glass()

    def draw_frame(self):
        """砂時計の枠を描画"""
        # トーラスのパラメータ
        radius_x = 0.4  # x方向の半径
        radius_z = 0.15  # z方向の半径
        
        # まず1本の支柱を描画（テスト用）
        glColor3f(*self.frame_color)
        
        # 支柱の開始点と終了点を定義
        # 下部トーラスの前面から上部トーラスの前面へ
        glPushMatrix()
        glRotatef(90, 1.0, 0.0, 0.0)  # 支柱を垂直方向に向ける
        glTranslatef(radius_x, 0.0, -0.5)  # 下部トーラスの位置に移動
        self.draw_cylinder(0.015, 1.0)  # 支柱を描画（長さ1.0で上下のトーラスを接続）
        glPopMatrix()
        
        # 楕円形のトーラスを描画
        for y, color in [(0.5, (0.0, 0.0, 1.0)), (-0.5, (0.0, 1.0, 0.0))]:
            glPushMatrix()
            glColor3f(*color)
            glTranslatef(0.0, y, 0.0)
            glRotatef(90, 1.0, 0.0, 0.0)
            self.draw_elliptical_torus(radius_x, radius_z, 0.015)
            glPopMatrix()

    def draw_glass(self):
        """砂時計のガラス部分を描画"""
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.95, 0.95, 1.0, 0.15)
        
        # 上部ガラス
        glPushMatrix()
        glTranslatef(0.0, 0.3, 0.0)
        self.draw_glass_half()
        glPopMatrix()
        
        # 下部ガラス
        glPushMatrix()
        glTranslatef(0.0, -0.3, 0.0)
        glRotatef(180, 1.0, 0.0, 0.0)
        self.draw_glass_half()
        glPopMatrix()
        
        # 中央のくびれ部分
        glPushMatrix()
        glRotatef(90, 1.0, 0.0, 0.0)
        self.draw_cylinder(0.02, 0.1)
        glPopMatrix()
        
        glDisable(GL_BLEND)

    def draw_sand(self):
        """砂を描画"""
        glColor3f(*self.sand_color)
        glPointSize(2.0)
        
        glBegin(GL_POINTS)
        for x, y, z in self.sand_particles:
            glVertex3f(x, y, z)
        glEnd()

    def update_sand(self):
        """砂の位置を更新"""
        if self.sand_in_upper > 0:
            # 新しい砂粒子を追加
            for _ in range(min(5, self.sand_in_upper)):
                # ランダムな位置に砂粒子を生成
                angle = np.random.random() * 2 * np.pi
                r = np.random.random() * 0.1
                x = r * np.cos(angle)
                z = r * np.sin(angle)
                y = 0.3  # 上部から開始
                
                self.sand_particles.append([x, y, z])
                self.sand_in_upper -= 1
        
        # 既存の砂粒子を更新
        new_particles = []
        for particle in self.sand_particles:
            x, y, z = particle
            
            # 重力による落下
            y -= 0.01
            
            # 下部の制限
            if y < -0.3:
                y = -0.3
            
            new_particles.append([x, y, z])
        
        self.sand_particles = new_particles
        self.update()

    def draw_cylinder(self, radius, height, segments=32):
        """円柱を描画"""
        glBegin(GL_QUAD_STRIP)
        for i in range(segments + 1):
            angle = 2.0 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(x, y, 0)
            glVertex3f(x, y, height)
        glEnd()
        
        # 上下の円を描画
        for z in [0, height]:
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(0, 0, z)
            for i in range(segments + 1):
                angle = 2.0 * math.pi * i / segments
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                glVertex3f(x, y, z)
            glEnd()

    def draw_cone(self, base_radius, top_radius, height, segments=32):
        """円錐を描画"""
        glBegin(GL_QUAD_STRIP)
        for i in range(segments + 1):
            angle = 2.0 * math.pi * i / segments
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            glVertex3f(base_radius * cos_a, base_radius * sin_a, 0)
            glVertex3f(top_radius * cos_a, top_radius * sin_a, height)
        glEnd()
        
        # 底面と上面の円を描画
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, 0)
        for i in range(segments + 1):
            angle = 2.0 * math.pi * i / segments
            glVertex3f(base_radius * math.cos(angle), base_radius * math.sin(angle), 0)
        glEnd()
        
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, height)
        for i in range(segments + 1):
            angle = 2.0 * math.pi * i / segments
            glVertex3f(top_radius * math.cos(angle), top_radius * math.sin(angle), height)
        glEnd()

    def draw_elliptical_torus(self, radius_x, radius_z, tube_radius, segments=32, sides=16):
        """楕円形のトーラスを描画"""
        for i in range(segments):
            angle1 = 2.0 * math.pi * i / segments
            angle2 = 2.0 * math.pi * (i + 1) / segments
            
            glBegin(GL_QUAD_STRIP)
            for j in range(sides + 1):
                theta = 2.0 * math.pi * j / sides
                
                cos_t = math.cos(theta)
                sin_t = math.sin(theta)
                cos_a1 = math.cos(angle1)
                sin_a1 = math.sin(angle1)
                cos_a2 = math.cos(angle2)
                sin_a2 = math.sin(angle2)
                
                # 楕円形の計算（x方向とz方向で異なる半径を使用）
                x = (radius_x + tube_radius * cos_t) * cos_a1
                y = tube_radius * sin_t
                z = (radius_z + tube_radius * cos_t) * sin_a1
                glVertex3f(x, y, z)
                
                x = (radius_x + tube_radius * cos_t) * cos_a2
                y = tube_radius * sin_t
                z = (radius_z + tube_radius * cos_t) * sin_a2
                glVertex3f(x, y, z)
                
            glEnd()

    def draw_glass_half(self):
        """砂時計の上下半分を描画"""
        # 円筒部分（上部）
        glPushMatrix()
        glRotatef(90, 1.0, 0.0, 0.0)
        self.draw_cylinder(0.2, 0.15)  # より広い円筒
        glPopMatrix()
        
        # 円錐部分（下部）
        glPushMatrix()
        glTranslatef(0.0, -0.15, 0.0)
        glRotatef(90, 1.0, 0.0, 0.0)
        self.draw_cone(0.2, 0.02, 0.25)  # より急な勾配の円錐
        glPopMatrix()

    def mousePressEvent(self, event):
        """マウスプレスイベント"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_pos = event.position()

    def mouseReleaseEvent(self, event):
        """マウスリリースイベント"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_pos = None

    def mouseMoveEvent(self, event):
        """マウスムーブイベント"""
        if self.last_pos is not None:
            current_pos = event.position()
            dx = current_pos.x() - self.last_pos.x()
            dy = current_pos.y() - self.last_pos.y()
            
            # 回転の更新
            self.rotation[1] += dx * 0.5
            self.rotation[0] += dy * 0.5
            
            self.last_pos = current_pos
            self.update()