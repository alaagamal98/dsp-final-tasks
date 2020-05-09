from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
from mainwindow import Ui_MainWindow
import plotly.express as px
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.FirstBubbleButton.clicked.connect(self.FirstBubbleGraph)
        self.ui.MapsButton.clicked.connect(self.MapsGraph)
        self.ui.SortedButton.clicked.connect(self.SortedGraph)
        self.ui.SecondBubbleButton.clicked.connect(self.SecondBubbleGraph)
        self.data = pd.read_excel('PreProcessedCOVID-192.xlsx', sheet_name='Sheet1')
        self.data['date']=self.data['date'].dt.strftime('%Y-%m-%d')

    def FirstBubbleGraph(self):
        fig = px.scatter(self.data,x="deaths", y="recovered",animation_frame="date", animation_group="country",
            color="continent", 
             size="cases", 
              hover_name="country",
              range_x=[-1000,60000]
              ,range_y=[-1000,125000], size_max=200)
        fig.show()
        # fig.write_html("file.html")
        # view = QWebEngineView()
        # view.load(QtCore.QUrl.fromLocalFile(r"file.html"))
        # view.show()
    def MapsGraph(self):

        fig = px.choropleth(self.data, hover_name="country", color="cases",
                           range_color=(0, 5000),
                            locations="countryterritoryCode",color_continuous_scale=px.colors.sequential.Plasma,animation_frame="date", animation_group="country")

        fig.show()

    def SortedGraph(self):
        fig = px.bar(self.data, y='deaths', x='country', animation_frame="date", animation_group="country",
            color="continent")
        fig.show()

    def SecondBubbleGraph(self):
        fig = px.scatter(self.data,x="deaths", y="recovered",animation_frame="date", animation_group="country",
            color="continent", 
             size="cases", 
              hover_name="country",
              range_x=[-1000,60000]
              ,range_y=[-1000,125000], size_max=200)
        fig.show()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow() 
    window.show()
    sys.exit(app.exec_())