from PyQt5 import QtWidgets,QtGui
from mainwindow import Ui_MainWindow
import sys

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Browse.clicked.connect(self.openImage)
        self.images =[self.ui.Image1,self.ui.Image2,self.ui.Image3,self.ui.Image4,self.ui.Image5,self.ui.Image6,self.ui.Image7,self.ui.Image8]
        self.upNibble=[]
        self.markers=[]
        self.huffDC=[0]*4
        self.huffAC=[0]*8
        self.id=[]

    def openImage(self):
        options =  QtWidgets.QFileDialog.Options()
        imgPath = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "", "(*jpeg)", options=options) 
        if(imgPath[0]!=''):
            self.data = open(imgPath[0],'rb').read()
            self.data = ''.join(['%02x,%02x,' % (self.data[2*i],self.data[2*i+1]) for i in range(len(self.data)>>1)])
            self.data = self.data.split(',')[:-1]
            self.huffmanTable() 
            self.decodeImage(imgPath[0])

    def decodeImage(self,path):
        pixmap = QtGui.QPixmap(path)
        self.images[0].setPixmap(pixmap)
        self.images[0].setScaledContents(True)
        markers= self.markerIndex('ffda')
        for i in range (8):
            imgByte=open(path,"rb").read(markers[i+1])
            output='Images/output.jpeg'
            outputData = open(output,"wb")
            outputData.write(imgByte)
            outputData.close()
            outputImage=QtGui.QImage(output)
            self.pixmapImage=QtGui.QPixmap.fromImage(outputImage).scaled(250,250)            
            self.images[i].setPixmap(self.pixmapImage)

    def huffmanTable(self):
        length=[]   
        valuesLegnth=[]
        byteSymbols=[]
        ACid=[]
        for m in range (8):
            ACid.append(m)
        self.markers=self.markerIndex("ffc4")
        for i in range (len(self.markers)):
            byteOffset=[]
            x=list(self.data[self.markers[i]+4])
            self.upNibble.append(x[0])
            self.id.append(x[1])
            y=int(self.data[self.markers[i]+2]+self.data[self.markers[i]+3],16)
            length.append(y)
            for j in range (16):
               offset=int(self.data[self.markers[i]+5+j],16) 
               byteOffset.append(offset)
            valuesLegnth.append(byteOffset[15])
            currentIndex=self.markers[i]+21
            subSymbols = []
            for k in range (16):    
                subSymbols.append(self.data[currentIndex:currentIndex+byteOffset[k]])
                currentIndex+=byteOffset[k]
            byteSymbols.append(subSymbols)
            if (self.upNibble[i]=='0'):
                self.huffDC[int(self.id[i])]=byteSymbols[i]
            elif(self.upNibble[i]=='1'):
                self.huffAC[ACid[i-2]]=byteSymbols[i]

    def markerIndex(self,marker):
        index=[]
        for i in range (len(self.data)-1):
            if (marker==self.data[i]+self.data[i+1]):
                index.append(i)
        return index


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow() 
    window.show()
    sys.exit(app.exec_())