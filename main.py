import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMenu, QAction, QDesktopWidget, QFileDialog, QVBoxLayout, QWidget, QPushButton, QFrame, QWidgetAction
from PyQt5.QtGui import QMovie, QCursor, QFont
from PyQt5.QtCore import Qt, QTimer, QTime
import os
import random

OUTPUT_PATH = './output'

class DesktopPet(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口为无边框和透明背景
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 初始化宠物标签
        self.pet_label = QLabel(self)
        self.pet_label.setScaledContents(True)  # 确保GIF可以根据标签大小缩放

        files = os.listdir(OUTPUT_PATH)
        image_files = [os.path.join(OUTPUT_PATH, file) for file in files if file.lower().endswith('.gif')]

        # 配置多个图标
        self.icons = image_files  # 使用你自己的GIF文件路径
        self.current_icon_index = random.randint(0, len(image_files) - 1)  # 当前显示的图标索引
        self.load_pet_icon(self.icons[self.current_icon_index])

        # 初始化专注功能
        self.focus_widget = None  # 专注功能的窗口
        self.timer = QTimer(self)  # 用于倒计时
        self.timer.timeout.connect(self.update_timer_display)
        self.remaining_time = QTime(0, 0, 0)  # 初始化剩余时间为 0

        # 初始化提醒文本标签
        self.reminder_label = QLabel("专注时间到了，休息一下吧！", self)
        self.reminder_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.reminder_label.setStyleSheet("""
            QLabel {
                color: red;
                font-size: 20px;
                font-weight: bold;
                background-color: yellow;
                padding: 5px;
                border: 2px solid red;
            }
        """)
        self.reminder_label.setAlignment(Qt.AlignCenter)
        self.reminder_label.hide()  # 初始状态隐藏

        self.reminder_timer = QTimer(self)  # 用于隐藏提醒标签的定时器
        self.reminder_timer.timeout.connect(self.hide_reminder)


        # 初始化鼠标跟踪和菜单
        self.is_following_mouse = False
        self.create_context_menu()  

        
    def load_pet_icon(self, icon_path):
        """加载和设置当前宠物图标"""
        self.movie = QMovie(icon_path)  # 加载GIF动画
        self.pet_label.setMovie(self.movie)
        self.movie.setCacheMode(QMovie.CacheAll)  # 缓存所有帧以提高性能
        self.movie.setSpeed(100)  # 设置播放速度（百分比）
        self.movie.loopCount()  # 设置循环次数，-1表示无限循环
        self.movie.start()  # 开始播放GIF

        # 设置窗口大小与GIF动图大小匹配
        self.pet_label.setGeometry(0, 0, self.movie.frameRect().width(), self.movie.frameRect().height())
        self.setFixedSize(self.movie.frameRect().size())

    def create_context_menu(self):
        """创建右键菜单"""
        self.contextMenu = QMenu(self)
        change_sys_icon_action = QAction('换一换', self)
        change_local_icon_action = QAction('换我的图', self)
        exit_action = QAction('退出', self)


         # 创建“专注”子菜单
        self.focus_menu = QMenu("专注", self)
        self.timer_display_action = QAction('0:00:00', self)  # 显示倒计时
        self.timer_display_action.setEnabled(False)  # 只用来显示时间，不可点击


        # 创建其他专注子菜单的选项
        self.start_focus_action = QAction('开始专注', self)
        self.add_time_action = QAction('加5分钟', self)
        self.subtract_time_action = QAction('减5分钟', self)
        self.stop_focus_action = QAction('结束专注', self)


        # 添加专注子菜单的选项
        self.focus_menu.addAction(self.timer_display_action)
        self.focus_menu.addAction(self.start_focus_action)
        self.focus_menu.addAction(self.add_time_action)
        self.focus_menu.addAction(self.subtract_time_action)
        self.focus_menu.addAction(self.stop_focus_action)

        # 添加动作到菜单
        self.contextMenu.addAction(change_sys_icon_action)
        self.contextMenu.addAction(change_local_icon_action)
        self.contextMenu.addMenu(self.focus_menu)  # 添加子菜单到主菜单
        self.contextMenu.addAction(exit_action)

        # 连接动作
        change_sys_icon_action.triggered.connect(self.change_sys_icon)
        change_local_icon_action.triggered.connect(self.change_local_icon)
        self.start_focus_action.triggered.connect(self.start_focus)
        self.add_time_action.triggered.connect(self.add_time)
        self.subtract_time_action.triggered.connect(self.subtract_time)
        self.stop_focus_action.triggered.connect(self.stop_focus)
        exit_action.triggered.connect(QApplication.quit)  # 退出程序

        # 更新菜单状态
        self.update_focus_controls()

    def start_focus(self):
        """开始专注倒计时"""
        self.remaining_time = QTime(0, 0, 5)  # 初始化为15分钟
        self.timer.start(1000)  # 每秒更新一次
        self.update_focus_controls()

    def add_time(self):
        """增加5分钟"""
        if self.timer.isActive():
            self.remaining_time = self.remaining_time.addSecs(5 * 60)
            self.update_timer_display()
        self.update_focus_controls()

    def subtract_time(self):
        """减少5分钟"""
        if self.timer.isActive() and self.remaining_time.minute() >= 5:
            self.remaining_time = self.remaining_time.addSecs(-5 * 60)
            self.update_timer_display()
        self.update_focus_controls()

    def stop_focus(self):
        """退出专注模式"""
        self.timer.stop()
        self.remaining_time = QTime(0, 0, 0)  # 重置时间
        self.update_timer_display()
        self.update_focus_controls()

    def update_timer_display(self):
        """更新倒计时显示"""
        if self.remaining_time > QTime(0, 0, 0):
            self.remaining_time = self.remaining_time.addSecs(-1)
        self.timer_display_action.setText(self.remaining_time.toString("hh:mm:ss"))  # 更新显示
        if self.remaining_time == QTime(0, 0, 0):
            self.timer.stop()  # 直接停止计时器
            self.remaining_time = QTime(0, 0, 0)  # 重置时间
            self.show_reminder()  # 显示提醒
            self.update_focus_controls()  # 更新控制状态


    def show_reminder(self):
        """显示休息提醒"""

        # 获取屏幕大小
        screen_rect = QDesktopWidget().availableGeometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()

        # 动图的当前全局位置
        pet_global_pos = self.mapToGlobal(self.pet_label.pos())
        pet_x = pet_global_pos.x()
        pet_y = pet_global_pos.y()

        # 动图的高度和宽度
        pet_height = self.pet_label.height()
        pet_width = self.pet_label.width()

        # 提醒文本的宽度和高度
        reminder_width = 300
        reminder_height = 50

        # 默认情况下，显示在动图的下方
        reminder_x = pet_x + (pet_width - reminder_width) // 2  # 水平居中于动图
        reminder_y = pet_y + pet_height + 10  # 动图下方10个像素

        # 检查下方空间是否足够
        if reminder_y + reminder_height > screen_height:  # 下方空间不足
            reminder_y = pet_y - reminder_height - 10  # 动图上方10个像素

        # 检查上方空间是否足够
        if reminder_y < 0:  # 上方空间不足
            reminder_y = pet_y + pet_height + 10  # 动图下方10个像素

        # 调整提醒文本的位置以确保在屏幕范围内
        if reminder_x < 0:  # 如果超出屏幕左侧
            reminder_x = 0
        elif reminder_x + reminder_width > screen_width:  # 如果超出屏幕右侧
            reminder_x = screen_width - reminder_width

        # 设置调整后的提醒文本位置
        self.reminder_label.setGeometry(reminder_x, reminder_y, reminder_width, reminder_height)

        # 显示提醒
        self.reminder_label.show()
        self.reminder_timer.start(5000)  # 5秒后自动隐藏提醒


    def hide_reminder(self):
        """隐藏休息提醒"""
        self.reminder_label.hide()
        self.reminder_timer.stop()


    def update_focus_controls(self):
        """根据倒计时状态更新按钮状态"""
        is_timing = self.timer.isActive()
        self.start_focus_action.setEnabled(not is_timing)  # 开始专注
        self.add_time_action.setEnabled(is_timing)  # 加5分钟
        self.subtract_time_action.setEnabled(is_timing and self.remaining_time.minute() >= 5)  # 减5分钟
        self.stop_focus_action.setEnabled(is_timing)  # 退出专注


    def change_local_icon(self):
        """更改图标功能"""
        # 打开文件对话框选择新的图标
        icon_path, _ = QFileDialog.getOpenFileName(self, "选择新的宠物图标", "", "GIF Files (*.gif)")
        if icon_path:
            # self.icons.append(icon_path)  # 将新的图标路径添加到列表中
            self.load_pet_icon(icon_path)  # 加载并设置新的图标

    def change_sys_icon(self):
        """随机更换系统自带动图"""
        self.current_icon_index = random.randint(0, len(self.icons) - 1) 
        self.load_pet_icon(self.icons[self.current_icon_index])

    def mousePressEvent(self, event):
        """鼠标按下事件处理"""
        if event.button() == Qt.LeftButton:
            self.is_following_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        elif event.button() == Qt.RightButton:
            self.contextMenu.exec_(QCursor.pos())  # 显示右键菜单


    def mouseMoveEvent(self, event):
        """鼠标移动事件处理"""
        if Qt.LeftButton and self.is_following_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()


    def mouseReleaseEvent(self, event):
        """鼠标释放事件处理"""
        self.is_following_mouse = False


    def changeImage(self):
        """修改图标"""
        # 打开文件对话框选择新的图标
        icon_path, _ = QFileDialog.getOpenFileName(self, "选择新的宠物图标", "", "GIF Files (*.gif)")
        if icon_path:
            self.icons.append(icon_path)  # 将新的图标路径添加到列表中
            self.load_pet_icon(icon_path)  # 加载并设置新的图标

    def center(self):
        """居中显示窗口"""
        screen_geometry = QDesktopWidget().screenGeometry()
        self.move((screen_geometry.width() - self.width()) // 2, (screen_geometry.height() - self.height()) // 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    pet.center()  # 居中显示
    sys.exit(app.exec_())
