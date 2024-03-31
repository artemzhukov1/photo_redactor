import os
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import (
        QListWidget, QFileDialog,
        QApplication, QWidget,
        QHBoxLayout, QVBoxLayout,
        QGroupBox, QButtonGroup, QRadioButton,
        QPushButton, QLabel)

def filter(files, extensions):
        result = []
        for filename in files:
                for ext in extensions:
                        if filename.endswith(ext):
                                result.append(filename)
        return result

workdir = " "

def chooseWorkdir():
        global workdir
        workdir = QFileDialog.getExistingDirectory()

def showFilenameList():
        chooseWorkdir()
        extensions = [".png", ".jpg", ".bmp"]
        filenames = filter(os.listdir(workdir), extensions)
        lw_image.clear()
        for filename in filenames:
                lw_image.addItem(filename)

app = QApplication([])
win =   QWidget()
win.resize(800,600)
win.setWindowTitle("Easy Editor")
lb_image = QLabel("Картинка")
btn_dir = QPushButton("Папка")
lw_image = QListWidget()

btn_left = QPushButton("Влево")
btn_right = QPushButton("Вправо")
btn_flip = QPushButton("Зеркало")
btn_sharp = QPushButton("Резкость")
btn_bw = QPushButton("Ч/Б")

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_image)
col2.addWidget(lb_image)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1)
row.addLayout(col2)
win.setLayout(row)

btn_dir.clicked.connect(showFilenameList)

class ImageProcessor():
        def __init__(self):
                self.image = None
                self.filename = None
                self.save_dir = "Modified/"

        def loadImage(self, filename):
                self.filename = filename
                image_path = os.path.join(workdir, filename)
                self.image = Image.open(image_path)

        def showImage(self, path):
                lb_image.hide()
                pixmapimage = QPixmap(path)
                w, h = lb_image.width(), lb_image.height()
                pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
                lb_image.setPixmap(pixmapimage)
                lb_image.show()

        def saveImage(self):
                path = os.path.join(workdir, self.save_dir)
                if not(os.path.exists(path) or os.path.isdir(path)):
                        os.mkdir(path)
                image_path = os.path.join(path, self.filename)
                self.image.save(image_path)

        def do_bw(self):
                self.image = self.image.convert("L")
                self.saveImage()
                image_path = os.path.join(workdir, self.save_dir, self.filename)
                self.showImage(image_path)

        def do_left(self):
                self.image = self.image.transpose(Image.ROTATE_90)
                self.saveImage()
                image_path = os.path.join(workdir, self.save_dir, self.filename)
                self.showImage(image_path)
        
        def do_right(self):
                self.image = self.image.transpose(Image.ROTATE_270)
                self.saveImage()
                image_path = os.path.join(workdir, self.save_dir, self.filename)
                self.showImage(image_path)  

        def do_sharp(self):
                self.image = self.image.filter(ImageFilter.BLUR)  
                self.saveImage()
                image_path = os.path.join(workdir, self.save_dir, self.filename)
                self.showImage(image_path) 

        def do_flip(self):
                self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
                self.saveImage()
                image_path = os.path.join(workdir, self.save_dir, self.filename)
                self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
        if lw_image.currentRow() >= 0:
                filename = lw_image.currentItem().text()
                workimage.loadImage(filename)
                image_path = os.path.join(workdir, workimage.filename)
                workimage.showImage(image_path)

lw_image.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharp)
btn_flip.clicked.connect(workimage.do_flip)

win.show()
app.exec()
