from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
class ShrinkableQlabel(QGraphicsView):

    mScene = QGraphicsScene()
    mPixmapItem = QGraphicsPixmapItem()
    mSource = QImage()
    mHighQuality = 1

    def __init__(self, parent):
        super(ShrinkableQlabel, self).__init__(parent)
        self.setup()
    def setup(self):
        self.setFocusPolicy(Qt.NoFocus)
        self.setFrameStyle(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        #setup
        fmt = QGLFormat()
        fmt.setSampleBuffers(False)
        fmt.setDoubleBuffer(True)
        fmt.setDirectRendering(True)
        fmt.setSwapInterval(1)
        fmt.setStencil(False)
        fmt.setRgba(False)
        fmt.setDepth(False)
        self.setupViewport(QGLWidget(fmt))
        self.viewport().setAttribute(Qt.WA_OpaquePaintEvent)
        self.viewport().setAttribute(Qt.WA_NoSystemBackground)

        self.mScene = QGraphicsScene(self)
        self.setScene(self.mScene)
        self.mPixmapItem = QGraphicsPixmapItem()
        self.mScene.addItem(self.mPixmapItem)

    def setHighQuality(self,high):
        self.mHighQuality = high

    def setImage(self,aPicture):
        self.mSource = aPicture
        self.displayImage()
        self.fitInView(0,0,self.mScene.width(),self.mScene.height(),Qt.KeepAspectRatio)

    def displayImage(self):
        pixmap = QPixmap.fromImage(self.mSource)
        self.mPixmapItem.setTransformationMode(Qt.SmoothTransformation if self.mHighQuality else Qt.FastTransformation)
        self.mPixmapItem.setPixmap(pixmap)
        self.mScene.setSceneRect(self.mPixmapItem.boundingRect())

    def getRenderSize(self):
        s = QSizeF(self.mScene.width(),self.mScene.height())
        ratio = 1.0
        if (self.mScene.height()>self.mScene.width()):
            ratio = (self.mScene.height()/self.height())

        else:
            ratio = (self.mScene.width()/self.width())

        if (ratio == 0):
            ratio = 1.0


        return s/ratio






