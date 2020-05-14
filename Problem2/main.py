from PyQt5 import QtWidgets,QtGui
from mainwindow import Ui_MainWindow
import cv2 as cv
import numpy as np
# from turbojpeg import TurboJPEG, TJPF_GRAY, TJSAMP_GRAY, TJFLAG_PROGRESSIVE
import 
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Browse.clicked.connect(self.getFile)
     

    def getFile(self):
        options =  QtWidgets.QFileDialog.Options()
        imgPath = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "", "(*jpg)", options=options) 
        if(imgPath[0]!=''):
            # jpeg = TurboJPEG()
            # Image = open('output_quality_100_progressive.jpg', 'wb')
            # Image.write(jpeg.encode(bgr_array, quality=100, flags=TJFLAG_PROGRESSIVE))
            # Image.close()
            print(Image)
        
    def showImage(self,image,component):
        cv.imwrite("results/edit.jpg", np.float64(image)) 
        pixmap = QtGui.QPixmap('results/edit.jpg')
        component.setPixmap(pixmap)
        component.setScaledContents(True)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow() 
    window.show()
    sys.exit(app.exec_())