from PyQt5 import QtWidgets,QtGui,QtCore,QtWebEngineWidgets
from mainwindow import Ui_MainWindow
import plotly.express as px
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import os
import sys

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.FirstBubbleButton.clicked.connect(self.FirstBubbleGraph)
        self.ui.MapsButton.clicked.connect(self.MapsGraph)
        self.ui.SortedButton.clicked.connect(self.SortedGraph)
        self.ui.SecondBubbleButton.clicked.connect(self.SecondBubbleGraph)
        self.data = pd.read_excel('Database/PreProcessedCOVID-192.xlsx', sheet_name='Sheet1')
        self.data['date']=self.data['date'].dt.strftime('%Y-%m-%d')

    def FirstBubbleGraph(self):
        fig = px.scatter(self.data,x="deaths", y="recovered",animation_frame="date", animation_group="country",
            color="continent", 
             size="cases", 
              hover_name="country", 
              range_x=[1,3000]
              ,range_y=[-500,10000],log_x=True, size_max=200)
        fileName="FirstBubbleGraph.html"
        fig.write_html("Graphs/"+fileName)
        self.setupGraph(fileName)
        self.Graph.show()

    def MapsGraph(self):

        fig = px.choropleth(self.data, hover_name="country", color="cases",
                           range_color=(0, 5000),
                            locations="countryterritoryCode",color_continuous_scale=px.colors.sequential.Plasma,animation_frame="date", animation_group="country")
        fileName="MapsGraph.html"
        fig.write_html("Graphs/"+fileName)
        self.setupGraph(fileName)
        self.Graph.show()


    def SortedGraph(self):
        fig = px.bar(self.data, y='cases',hover_name="country", x='countryterritoryCode', animation_frame="date", animation_group="country",
            color="continent")
        fig.update_layout( xaxis={'categoryorder':'total descending'})
        fileName="SortedGraph.html"
        fig.write_html("Graphs/"+fileName)
        self.setupGraph(fileName)
        self.Graph.show()

    def SecondBubbleGraph(self):
        fig = px.scatter(self.data,x="deaths", y="recovered",animation_frame="date", animation_group="country",
            color="continent", 
             size="cases", 
              hover_name="country",
              range_x=[1,3000]
              ,range_y=[-500,10000],log_x=True, size_max=200)
        fileName="SecondBubbleGraph.html"
        fig.write_html("Graphs/"+fileName)
        self.setupGraph(fileName)
        self.Graph.show()



    def setupGraph(self,fileName):
        self.Graph = QtWidgets.QWidget()
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.Graph)
        self.webEngineView.setGeometry(QtCore.QRect(-1, 0, 1000, 750))
        path= os.path.abspath(os.path.join(os.path.dirname(__file__),"Graphs/"+fileName))
        self.webEngineView.setUrl(QtCore.QUrl.fromLocalFile(path))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow() 
    window.show()
    sys.exit(app.exec_())