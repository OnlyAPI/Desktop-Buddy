import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMenu, QAction, QDesktopWidget, QFileDialog, QVBoxLayout, QWidget, QPushButton, QFrame, QWidgetAction
from PyQt5.QtGui import QMovie, QCursor
from PyQt5.QtCore import Qt, QTimer, QTime

class DesktopPet(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口为无边框和透明背景
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 初始化宠物标签
        self.pet_label = QLabel(self)
        self.pet_label.setScaledContents(True)  # 确保GIF可以根据标签大小缩放

        # 配置多个图标
        self.icons = ["./images/pet.gif"]  # 使用你自己的GIF文件路径
        self.current_icon_index = 0  # 当前显示的图标索引
        self.load_pet_icon(self.icons[self.current_icon_index])

        # 初始化专注功能
        self.focus_widget = None  # 专注功能的窗口
        self.timer = QTimer(self)  # 用于倒计时
        self.timer.timeout.connect(self.update_timer_display)
        self.remaining_time = QTime(0, 0, 0)  # 初始化剩余时间为 0

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
        change_icon_action = QAction('更换图标', self)
        exit_action = QAction('退出', self)


         # 创建“专注”子菜单
        self.focus_menu = QMenu("专注", self)
        self.timer_display_action = QAction('0:00:00', self)  # 显示倒计时
        self.timer_display_action.setEnabled(False)  # 只用来显示时间，不可点击


        # 创建一个带有分隔线的部件
        self.separator_action = QWidgetAction(self)
        separator_widget = QWidget(self)  # 用 QWidget 包装 QFrame
        layout = QVBoxLayout(separator_widget)  # 使用垂直布局
        layout.setContentsMargins(0, 5, 0, 5)  # 设置上下边距，确保分隔线显示
        layout.setSpacing(0)  # 去除控件之间的间隔
        
        # 创建 QFrame 作为分隔线
        separator_line = QFrame(separator_widget)
        separator_line.setFrameShape(QFrame.HLine)  # 水平线
        separator_line.setFrameShadow(QFrame.Sunken)  # 凹陷效果
        separator_line.setFixedHeight(2)  # 设置分隔线高度
        separator_line.setStyleSheet("background-color: #FF0000;")  # 设置分隔线颜色
        layout.addWidget(separator_line)  # 将分隔线添加到布局中

        self.separator_action.setDefaultWidget(separator_widget)  # 设置分隔线的默认小部件

        # 创建其他专注子菜单的选项
        self.start_focus_action = QAction('开始专注', self)
        self.add_time_action = QAction('加5分钟', self)
        self.subtract_time_action = QAction('减5分钟', self)
        self.stop_focus_action = QAction('结束专注', self)


        # 添加专注子菜单的选项
        self.focus_menu.addAction(self.timer_display_action)
        self.focus_menu.addAction(self.separator_action)  # 添加分隔线
        self.focus_menu.addAction(self.start_focus_action)
        self.focus_menu.addAction(self.add_time_action)
        self.focus_menu.addAction(self.subtract_time_action)
        self.focus_menu.addAction(self.stop_focus_action)

        # 添加动作到菜单
        self.contextMenu.addAction(change_icon_action)
        self.contextMenu.addMenu(self.focus_menu)  # 添加子菜单到主菜单
        self.contextMenu.addAction(exit_action)

        # 连接动作
        change_icon_action.triggered.connect(self.change_icon)
        self.start_focus_action.triggered.connect(self.start_focus)
        self.add_time_action.triggered.connect(self.add_time)
        self.subtract_time_action.triggered.connect(self.subtract_time)
        self.stop_focus_action.triggered.connect(self.stop_focus)
        exit_action.triggered.connect(QApplication.quit)  # 退出程序

        # 更新菜单状态
        self.update_focus_controls()

    def start_focus(self):
        """开始专注倒计时"""
        self.remaining_time = QTime(0, 15, 0)  # 初始化为15分钟
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
            self.stop_focus()

    def update_focus_controls(self):
        """根据倒计时状态更新按钮状态"""
        is_timing = self.timer.isActive()
        self.start_focus_action.setEnabled(not is_timing)  # 开始专注
        self.add_time_action.setEnabled(is_timing)  # 加5分钟
        self.subtract_time_action.setEnabled(is_timing and self.remaining_time.minute() >= 5)  # 减5分钟
        self.stop_focus_action.setEnabled(is_timing)  # 退出专注


    def change_icon(self):
        """更改图标功能"""
        # 打开文件对话框选择新的图标
        icon_path, _ = QFileDialog.getOpenFileName(self, "选择新的宠物图标", "", "GIF Files (*.gif)")
        if icon_path:
            self.icons.append(icon_path)  # 将新的图标路径添加到列表中
            self.load_pet_icon(icon_path)  # 加载并设置新的图标


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


    def speak(self):
        """说话功能"""
        print("宠物说：你好！")


    def jump(self):
        """跳跃功能"""
        print("宠物跳跃！")


    def changeImage(self):
        """修改图标"""
        # 打开文件对话框选择新的图标
        icon_path, _ = QFileDialog.getOpenFileName(self, "选择新的宠物图标", "", "GIF Files (*.gif)")
        if icon_path:
            self.icons.append(icon_path)  # 将新的图标路径添加到列表中
            self.load_pet_icon(icon_path)  # 加载并设置新的图标

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec_())
