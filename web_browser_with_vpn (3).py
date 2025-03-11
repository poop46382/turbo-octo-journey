import sys
import subprocess
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget,
    QLineEdit, QLabel, QToolBar, QAction, QStatusBar, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Browser with VPN")
        self.setGeometry(200, 200, 1024, 768)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.url_bar)
        self.layout.addWidget(self.browser)

        self.vpn_label = QLabel("VPN Status: Disconnected")
        self.vpn_button = QPushButton("Connect VPN")
        self.vpn_button.clicked.connect(self.toggle_vpn)

        self.layout.addWidget(self.vpn_label)
        self.layout.addWidget(self.vpn_button)

        self.init_ui()

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.vpn_process = None

    def init_ui(self):
        # Creating a toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        back_action = QAction("Back", self)
        back_action.triggered.connect(self.browser.back)
        toolbar.addAction(back_action)

        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(self.browser.forward)
        toolbar.addAction(forward_action)

        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(self.browser.reload)
        toolbar.addAction(reload_action)

        home_action = QAction("Home", self)
        home_action.triggered.connect(self.navigate_home)
        toolbar.addAction(home_action)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.browser.urlChanged.connect(self.update_url)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def toggle_vpn(self):
        if self.vpn_process:
            self.vpn_process.terminate()
            self.vpn_process = None
            self.vpn_label.setText("VPN Status: Disconnected")
            self.vpn_button.setText("Connect VPN")
            self.status.showMessage("VPN Disconnected", 5000)
        else:
            try:
                self.vpn_process = subprocess.Popen(["openvpn", "--config", "path/to/your/vpn/config.ovpn"])
                self.vpn_label.setText("VPN Status: Connected")
                self.vpn_button.setText("Disconnect VPN")
                self.status.showMessage("VPN Connected", 5000)
            except Exception as e:
                QMessageBox.critical(self, "VPN Error", f"Failed to connect to VPN: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())