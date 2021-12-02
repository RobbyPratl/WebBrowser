import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from PyQt5.QtPrintSupport import *
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)
        self.status = QStatusBar()
        self.setStatusBar(self.status)


        navbar = QToolBar()
        self.addToolBar(navbar)

        refreshBtn = QAction(self)
        refreshBtn.triggered.connect(lambda: self.tabs.currentWidget().reload)
        refreshBtn.setIcon(QIcon("refresh-button.png"))
        navbar.addAction(refreshBtn)


        back_btn = QAction('Back',self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back)
        back_btn.setIcon(QIcon("backward.png"))
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward',self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward)
        forward_btn.setIcon(QIcon("forward.png"))
        navbar.addAction(forward_btn)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.urlbar)

        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        self.show()

        self.setWindowTitle("RobBrowser")

    def loadUrl(self):
        url = self.addressLineEditor.text()
        self.browser.setUrl(QUrl(url))

    def updateUrl(self,url):
        self.addressLineEditor.setText(url.toString())

        def add_new_tab(self, qurl = None, label ="Blank"):
 
        # if url is blank
            if qurl is None:
                qurl = QUrl('http://www.google.com')
 
        # creating a QWebEngineView object
        browser = QWebEngineView()
 
        # setting url to browser
        browser.setUrl(qurl)
 
        # setting tab index
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
 
        # adding action to the browser when url is changed
        # update the url
        browser.urlChanged.connect(lambda qurl, browser = browser:
            self.update_urlbar(qurl, browser))
 
        # adding action to the browser when loading is finished
        # set the tab title
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
            self.tabs.setTabText(i, browser.page().title()))
 
    # when double clicked is pressed on tabs
    def tab_open_doubleclick(self, i):
 
        # checking index i.e
        # No tab under the click
        if i == -1:
            # creating a new tab
            self.add_new_tab()
 
    # when tab is changed
    def current_tab_changed(self, i):
 
        # get the curl
        qurl = self.tabs.currentWidget().url()
 
        # update the url
        self.update_urlbar(qurl, self.tabs.currentWidget())
 
        # update the title
        self.update_title(self.tabs.currentWidget())
 
    # when tab is closed
    def close_current_tab(self, i):
 
        # if there is only one tab
        if self.tabs.count() < 2:
            # do nothing
            return
 
        # else remove the tab
        self.tabs.removeTab(i)
 
    # method for updating the title
    def update_title(self, browser):
 
        # if signal is not from the current tab
        if browser != self.tabs.currentWidget():
            # do nothing
            return
 
        # get the page title
        title = self.tabs.currentWidget().page().title()
 
        # set the window title
        self.setWindowTitle("% s - Geek PyQt5" % title)
 
    # action to go to home
    def navigate_home(self):
 
        # go to google
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))
 
    # method for navigate to url
    def navigate_to_url(self):
 
        # get the line edit text
        # convert it to QUrl object
        q = QUrl(self.urlbar.text())
 
        # if scheme is blank
        if q.scheme() == "":
            # set scheme
            q.setScheme("http")
 
        # set the url
        self.tabs.currentWidget().setUrl(q)
 
    # method to update the url
    def update_urlbar(self, q, browser = None):
 
        # If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
 
            return
 
        # set text to the url bar
        self.urlbar.setText(q.toString())
 
        # set cursor position
        self.urlbar.setCursorPosition(0)
        
app = QApplication(sys.argv)
QApplication.setApplicationName('Rob Browser')
window = MainWindow()
app.exec_()