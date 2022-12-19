# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qrcode
import sys

class Image(qrcode.image.base.BaseImage):
	
    def __init__(self, border, width, box_size):

        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QImage(size, size, QImage.Format_RGB16)
        self._image.fill(QColor("#FFFF00"))
 
    def pixmap(self):

        return QPixmap.fromImage(self._image)
 
    def drawrect(self, row, col):

        painter = QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            QtCore.Qt.black)

class Screen(QWidget):
	def __init__(self):
		super(Screen, self).__init__()
		self.layout = QVBoxLayout()
		self.layout.addWidget(Title(self))
		self.setLayout(self.layout)
		self.layout.setContentsMargins(0,0,0,0)
		self.layout.addStretch(-1)
		self.setMinimumSize(300,400)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.pressing = False

		self.label = QLabel(self)
		self.edit = QLineEdit()
		self.edit.returnPressed.connect(self.handleTextEntered)
		self.edit.setFont(QFont('Time', 9))
		self.edit.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(self.label)
		self.layout.addWidget(self.edit)

	def handleTextEntered(self):
		text = self.edit.text()
		qr_image = qrcode.make(text, image_factory = Image).pixmap()
		self.label.setPixmap(qr_image)

class Title(QWidget):
	def __init__(self, parent):
		super(Title, self).__init__()
		self.parent = parent 
		print(self.parent.width())
		self.layout = QHBoxLayout()
		self.layout.setContentsMargins(0,0,0,0)
		self.title=QLabel("QR Code Generator")

		self.closeBtn = QPushButton()
		self.closeBtn.setIcon(QIcon("C:/Users/skvit/Desktop/Browser/icons/close.png"))
		self.closeBtn.setFixedSize(30,40)
		self.closeBtn.setStyleSheet("border-radius: 50%;")
		self.closeBtn.clicked.connect(self.closeBtnClicked)

		self.minBtn = QPushButton()
		self.minBtn.setIcon(QIcon("C:/Users/skvit/Desktop/Browser/icons/minimize.png"))
		self.minBtn.setFixedSize(30,40)
		self.minBtn.setStyleSheet("border-radius: 50%;")
		self.minBtn.clicked.connect(self.minBtnClicked)

		self.title.setFixedHeight(40)
		self.layout.addWidget(self.title)
		self.layout.addWidget(self.minBtn)
		# self.layout.addWidget(self.maxBtn)
		self.layout.addWidget(self.closeBtn)

		self.title.setStyleSheet("""
			background-color: #88edf5;
			color: #303c54;
			font: Georgia;
			font-size: 20px;
		""")
		self.setLayout(self.layout)

		self.start = QPoint(0,0)
		self.pressing = False

	def resizeEvent(self, QResizeEvent):
		super(Title, self).resizeEvent(QResizeEvent)
		self.title.setFixedWidth(self.parent.width())

	def mousePressEvent(self, event):
		self.start = self.mapToGlobal(event.pos())
		self.pressing = True
	
	def mouseMoveEvent(self, event):
		if self.pressing:
			self.end = self.mapToGlobal(event.pos())
			self.movement = self.end-self.start
			self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
								self.mapToGlobal(self.movement).y(),
								self.parent.width(),
								self.parent.height())
			self.start = self.end
	
	def mouseReleaseEvent(self, QMouseEvent):
		self.pressing = False
	
	def closeBtnClicked(self):
		self.parent.close()
	
	def minBtnClicked(self):
		self.parent.showMinimized()