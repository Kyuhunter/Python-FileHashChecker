import hashlib
import sys

from PyQt6.QtWidgets import QApplication, QLabel, QFileDialog, QWidget, QPushButton, QVBoxLayout, QLineEdit


class FileDropper(QLabel):

    def __init__(self, parent):
        super(FileDropper, self).__init__(parent)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        data = e.mimeData()
        urls = data.urls()
        filepath = ""
        if urls and urls[0].scheme() == 'file':
            filepath = str(urls[0].path())[1:]

        self.setText(filepath)


class FileHashCheckerApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Hash Checker")
        self.setGeometry(0, 0, 600, 300)

        self.labelFileDropper = FileDropper("Datei auswählen")
        #self.selectFileButton.clicked.connect(self.get_file_to_check)
        self.labelFileDropper.setAcceptDrops(True)
        self.labelFileDropper.setStyleSheet("border: 1px solid black; border-radius: 15px; text-align: center; "
                                            "height: 200px")
        self.labelFileDropper.move(0, 0)
        self.labelFileDropper.resize(500, 150)

        self.labelMD5Hash = QLabel("Bitte zu vergleichenden MD5 Hash eingeben:")

        self.textMD5Hash = QLineEdit()

        self.buttonCompareMD5 = QPushButton('MD5 Vergleichen')
        self.buttonCompareMD5.clicked.connect(self.compare_md5)

        self.labelIsSame = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.labelFileDropper)
        layout.addWidget(self.labelMD5Hash)
        layout.addWidget(self.textMD5Hash)
        layout.addWidget(self.buttonCompareMD5)
        layout.addWidget(self.labelIsSame)

        self.setLayout(layout)

    def get_file_to_check(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Datei auswählen')
        self.labelFilePath.setText(file_name)

    def compare_md5(self):
        given_hash = self.textMD5Hash.text()
        generated_hash = md5(self.selectFileButton.text())

        if given_hash.upper() == generated_hash.upper():
            self.labelIsSame.setText('True')
            self.labelIsSame.setStyleSheet("background-color: green")
        else:
            self.labelIsSame.setText('False: ' + generated_hash.upper())
            self.labelIsSame.setStyleSheet("background-color: red")


def md5(fname):
    file_hash = hashlib.sha256()  # Create the hash object, can use something other than `.sha256()` if you wish
    with open(fname, 'rb') as f:  # Open the file to read it's bytes
        fb = f.read(65536)  # Read from the file. Take in the amount declared above
        while len(fb) > 0:  # While there is still data being read from the file
            file_hash.update(fb)  # Update the hash
            fb = f.read(65536)  # Read the next block from the file
    return file_hash.hexdigest()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = FileHashCheckerApp()
    demo.show()

    sys.exit(app.exec())
