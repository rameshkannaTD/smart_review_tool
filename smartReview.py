import sys

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from review_tool_UI.reviewToolUI import Ui_Form

COLORS = [
            '#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
            '#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
            '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff', '#ff0000',
        ]


class ImageBoard(QWidget):
    def __init__(self):
        super(ImageBoard, self).__init__()

        self.label = QLabel()
        self.image = QPixmap("review_image.jpg")
        self.label.setMaximumHeight(self.image.height())
        self.label.setMaximumWidth(self.image.width())
        self.label.setPixmap(self.image)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.last_point = None
        self.pen_color = "#000000"
        self.pen_size = 2
        self.erase = False
        self._clear_size = 20

    def set_pen_color(self, color):
        self.pen_color = color

    def set_pen_size(self, size):
        self.pen_size = size

    def set_eraser(self, value):
        self.erase = value

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = self.label.mapFromParent(event.pos())

    def mouseMoveEvent(self, event):
        end_point = self.label.mapFromParent(event.pos())
        painter = QPainter(self.label.pixmap())
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(
            QPen(
                QColor(self.pen_color),
                self.pen_size,
                Qt.SolidLine,
                Qt.RoundCap,
                Qt.RoundJoin
            )
        )
        if self.erase:
            print("eraser_enable")
            r = QRect(QPoint(), self._clear_size * QSize())
            r.moveCenter(end_point)
            painter.save()
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.eraseRect(r)
            painter.restore()
        else:
            line = QLine(self.last_point, end_point)
            painter.drawLine(line)
        self.last_point = end_point
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = None


class QPaletteButton(QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(35, 35))
        self.color = color
        self.setStyleSheet("background-color: {};".format(color))


class ReviewTool(Ui_Form, QWidget):
    def __init__(self):
        super(ReviewTool, self).__init__()
        self.setupUi(self)
        self.image_board = ImageBoard()
        self.resize(self.image_board.image.width(), self.image_board.image.height())
        self.verticalLayout_5.addWidget(self.image_board)
        self.brush_size_slider.valueChanged.connect(self.set_pen_size)
        self.color_pushbutton.setIcon(QIcon(r"D:\PythonProjects\NukePython\smart_review_tool\icons\color_wheel.png"))
        self.color_pushbutton.clicked.connect(self.open_color_panel)
        self.eraser_pushbutton.clicked.connect(self.enable_eraser)
        self.pen_pushbutton.clicked.connect(self.enable_pen)
        self.add_palette_button()

    def add_palette_button(self):
        for count, color in enumerate(COLORS):
            palette_button = QPaletteButton(color)
            palette_button.pressed.connect(lambda c=color: self.image_board.set_pen_color(c))
            palette_button.pressed.connect(lambda c=color: self.set_button_color(c))
            if count == 1:
                self.palette_layout.addWidget(palette_button, 0, 1)
            else:
                self.palette_layout.addWidget(palette_button)

    def open_color_panel(self):
        color_dialog = QColorDialog.getColor()
        self.image_board.set_pen_color(color_dialog)

        self.set_button_color(color_dialog.name())

    def set_button_color(self, hex):
        style_sheet = "background-color : {}".format(hex)
        self.color_pushbutton.setStyleSheet(style_sheet)

    def set_pen_size(self):
        pen_size = self.brush_size_slider.value()
        self.image_board.set_pen_size(pen_size)

    def enable_eraser(self):
        self.image_board.set_eraser(True)

    def enable_pen(self):
        self.image_board.set_eraser(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tool = ReviewTool()
    tool.show()
    sys.exit(app.exec_())
