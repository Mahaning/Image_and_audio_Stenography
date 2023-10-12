import os
import sys
import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets
import lsb_steganography as stego
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QApplication, QMainWindow, QPushButton, QFileDialog, QLabel,QVBoxLayout
from PIL import Image
from PyQt5.uic import loadUi
import subprocess


class Ui_PageAfterLogin(object):
    def setupUi(self, PageAfterLogin):
        text_color = "color: white;"
        PageAfterLogin.setObjectName("PageAfterLogin")
        PageAfterLogin.resize(620, 480)

        self.centralwidget = QtWidgets.QWidget(PageAfterLogin)
        self.centralwidget.setObjectName("centralwidget")

        self.text_encryption_button = QtWidgets.QPushButton(self.centralwidget)
        self.text_encryption_button.setGeometry(QtCore.QRect(50, 50, 150, 50))
        self.text_encryption_button.setStyleSheet(text_color)
        self.text_encryption_button.setObjectName("text_encryption_button")
        self.text_encryption_button.setText("Text Encryption")
        self.text_encryption_button.clicked.connect(self.show_text_encryption_page)

        self.audio_encryption_button = QtWidgets.QPushButton(self.centralwidget)
        self.audio_encryption_button.setGeometry(QtCore.QRect(50, 120, 150, 50))
        self.audio_encryption_button.setStyleSheet(text_color)
        self.audio_encryption_button.setObjectName("audio_encryption_button")
        self.audio_encryption_button.setText("Audio Encryption")
        self.audio_encryption_button.clicked.connect(self.show_audio_encription_page)

        PageAfterLogin.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(PageAfterLogin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 400, 21))
        self.menubar.setObjectName("menubar")

        PageAfterLogin.setMenuBar(self.menubar)

        # Apply the same background image and styling as the login page
        PageAfterLogin.setStyleSheet("background-image: url(img1.jpg);")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)


class PageAfterLogin(QtWidgets.QMainWindow, Ui_PageAfterLogin):
    def __init__(self):
        super(PageAfterLogin, self).__init__()
        self.setupUi(self)
        self.audio_encryption_button.clicked.connect(self.show_audio_encription_page)
        self.audio_app = None
        

    def show_text_encryption_page(self):
        # self.close()  # Close the current window
        self.main_window = QtWidgets.QMainWindow()
        ui = Text_Encription_Page()
        ui.setupUi(self.main_window)
        self.main_window.show()

    # def show_audio_encription_page(self):
        # self.close()  # Close the current window
        # self.main_window = QtWidgets.QMainWindow()
        # audio_app = AudioSteganographyApp()
        # audio_app.init_ui()
        # audio_app.show()
        # app.exec_()
        # ui = AudioSteganographyApp()
        # ui.init_ui(self.main_window)
        # self.main_window.show()
    def show_audio_encription_page(self):
        # Check if the audio app instance exists
        if self.audio_app is None:
            # Create an instance of AudioSteganographyApp
            self.audio_app = AudioSteganographyApp()
            # Initialize the audio steganography interface
            self.audio_app.init_ui()

        # Show the audio steganography interface
        self.audio_app.show()
        

      
class Text_Encription_Page(object):
    #Function to display message/error/information
    def displayMsg(self,title,msg,ico_type=None):
        MsgBox = QtWidgets.QMessageBox()
        MsgBox.setText(msg)
        MsgBox.setWindowTitle(title)
        if ico_type == 'err':
            ico = QtWidgets.QMessageBox.Critical
        else:
            ico = QtWidgets.QMessageBox.Information
        MsgBox.setIcon(ico)
        MsgBox.exec()

    #Function to choose input file
    def getFile(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(None, 'Open file','',"Image files (*.jpg *.png *.bmp)")[0]
        if file_path != '':
            self.lineEdit.setText(file_path)

    #Function to display save file dialog
    def saveFile(self):
        output_path = QtWidgets.QFileDialog.getSaveFileName(None, 'Save encoded file','',"PNG File(*.png)")[0]
        return output_path

    #Function to encode data and save file
    def encode(self):
        input_path = self.lineEdit.text()
        text = self.plainTextEdit.toPlainText()
        password = self.lineEdit_2.text()
        if input_path == '':
            self.displayMsg('Error: No file chosen','You must select input image file!','err')
        elif text == '':
            self.displayMsg('Text is empty','Please enter some text to hide!')
        elif password == '':
            self.displayMsg('Error: No password given','Please enter a password!','err')
        else:
            output_path = self.saveFile()
            if output_path == '':
                self.displayMsg('Operation cancelled','Operation cancelled by user!')
            else:
                try:
                    loss = stego.encode(input_path,text,output_path,password)
                except stego.FileError as fe:
                    self.displayMsg('File Error',str(fe),'err')
                except stego.DataError as de:
                    self.displayMsg('Data Error',str(de),'err')
                else:
                    self.displayMsg('Success','Encoded Successfully!\n\nImage Data Loss = {:.5f} %'.format(loss))
                    self.progressBar.setValue(0)

    #Function to decode data
    def decode(self):
        input_path = self.lineEdit.text()
        password = self.lineEdit_3.text()
        if input_path == '':
            self.displayMsg('Error: No file chosen','You must select input image file!','err')
        elif password == '':
            self.displayMsg('Error: No password given','Please enter a password!','err')
        else:
            try:
                data = stego.decode(input_path,password)
            except stego.FileError as fe:
                self.displayMsg('File Error',str(fe),'err')
            except stego.PasswordError as pe:
                self.displayMsg('Password Error',str(pe),'err')
                self.progressBar_2.setValue(0)
            else:
                self.displayMsg('Success','Decoded successfully!')
                self.plainTextEdit_2.document().setPlainText(data)
                self.progressBar_2.setValue(0)
    
    def setupUi(self, MainWindow):
        text_color = "color: white;"
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(811, 575)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-image: url(img4.jpg);repea")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.setStyleSheet()
        
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setAutoDefault(True)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setStyleSheet(text_color)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_3.addWidget(self.checkBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_6.addWidget(self.label_11)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_6.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem7)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2, 0, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem8)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem9)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setStyleSheet(text_color)
        self.horizontalLayout_4.addWidget(self.lineEdit_3)
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_4.addWidget(self.checkBox_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem10)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_4.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignHCenter)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem11)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_7.addWidget(self.label_13)
        self.progressBar_2 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_2.setEnabled(True)
        self.progressBar_2.setMaximum(100)
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setTextVisible(True)
        self.progressBar_2.setObjectName("progressBar_2")
        self.horizontalLayout_7.addWidget(self.progressBar_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem12)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_3.addWidget(self.label_12)
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.plainTextEdit_2.setStyleSheet(text_color)
        self.verticalLayout_3.addWidget(self.plainTextEdit_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem13)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem14)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 811, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        text_color = "color: white;"
    
        self.label.setStyleSheet(text_color)
        self.label_2.setStyleSheet(text_color)
        self.label_5.setStyleSheet(text_color)
        self.label_7.setStyleSheet(text_color)
        self.label_8.setStyleSheet(text_color)
        self.label_9.setStyleSheet(text_color)
        self.label_11.setStyleSheet(text_color)
        self.label_6.setStyleSheet(text_color)
        self.label_10.setStyleSheet(text_color)
        self.label_13.setStyleSheet(text_color)
        self.label_12.setStyleSheet(text_color)
        
        self.label_3.setStyleSheet(text_color)  # Modify the label for input field
        self.label_4.setStyleSheet(text_color)  # Modify the label for input field
        
        # self.lineEdit.setStyleSheet(text_color)  # Modify the input field
        # self.lineEdit_2.setStyleSheet(text_color)  # Modify the input field
        # self.lineEdit_3.setStyleSheet(text_color)  # Modify the input field

        # input_field_style = "background-color: rgba(255, 255, 255, 100); border: 1px solid white; border-radius: 10px; padding: 5px;"

        input_field_style = "background-color: white; border: 1px solid white; border-radius: 10px; padding: 5px;"

        self.lineEdit.setStyleSheet(input_field_style)  # Modify the input field
        self.lineEdit_2.setStyleSheet(input_field_style)  # Modify the input field
        self.lineEdit_3.setStyleSheet(input_field_style)
        
        

        #Slots
        self.pushButton.clicked.connect(self.getFile)
        self.pushButton_2.clicked.connect(self.encode)
        self.pushButton_3.clicked.connect(self.decode)
        self.checkBox.stateChanged.connect(lambda: self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal) if self.checkBox.isChecked() else self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password))
        self.checkBox_2.stateChanged.connect(lambda: self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Normal) if self.checkBox_2.isChecked() else self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password))

        #Menu action
        self.actionAbout.triggered.connect(lambda: self.displayMsg('About','Created by: Your Name\n\n'))
        
        
        


    def retranslateUi(self, MainWindow):
        text_color = "color: white;"
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Steganography Software"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Step 1:</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "Input Image File:"))
        self.pushButton.setStyleSheet(text_color)
        self.pushButton.setText(_translate("MainWindow", "Choose File"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#5500ff;\">Encode</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#5500ff;\">Decode</span></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Step 2:</span></p></body></html>"))
        
        self.label_7.setText(_translate("MainWindow", "Enter text to hide:"))

        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Step 3:</span></p></body></html>"))
        self.label_9.setText(_translate("MainWindow", "Enter Password:"))
        self.checkBox.setStyleSheet(text_color)
        self.checkBox.setText(_translate("MainWindow", "Show Password "))
        self.label_11.setStyleSheet(text_color)
        self.label_11.setText(_translate("MainWindow", "Progress:"))
        self.pushButton_2.setStyleSheet(text_color)
        self.pushButton_2.setText(_translate("MainWindow", "Encode and Save"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Step 2:</span></p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "Enter Password:"))
        self.checkBox_2.setStyleSheet(text_color)
        self.checkBox_2.setText(_translate("MainWindow", "Show Password"))
        self.pushButton_3.setStyleSheet(text_color)
        self.pushButton_3.setText(_translate("MainWindow", "Decode"))
        self.label_13.setStyleSheet(text_color)
        self.label_13.setText(_translate("MainWindow", "Progress:"))
        self.label_12.setText(_translate("MainWindow", "Decoded Data:"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

class AudioSteganographyApp(QMainWindow):
    def display_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setObjectName("PageAfterLogin")
        self.resize(620, 480)
        self.setWindowTitle("Audio Steganography")

        background_image = QtGui.QPixmap("bggg78.jpg")  # Replace with your image path
        background_image_label = QLabel(self)
        background_image_label.setPixmap(background_image)
        background_image_label.setGeometry(0, 0, self.width(), self.height())

        note_text = "Note:\nSTEP 1: Select an image in which you want to hide audio.\nSTEP 2: Select the audio you want to encrypt."
        self.note_label = QLabel(note_text, self)
        self.note_label.setGeometry(20, 20, 580, 60)
        self.note_label.setAlignment(QtCore.Qt.AlignLeft)
        self.note_label.setStyleSheet("color: white;")

        # Create a label for displaying messages
        self.label = QLabel(self)
        self.label.setGeometry(20, 80, 580, 40)
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.label.setStyleSheet("color: white;")

        self.btn_hide = QPushButton("Hide Audio", self)
        self.btn_hide.setGeometry(240, 140, 120, 40)
        self.btn_hide.clicked.connect(self.hide_audio)

        button_spacing = 80

        extract_audio_note = "Note:\nSTEP 1: Select an image from which you want to decrypt audio."
        self.extract_audio_note_label = QLabel(extract_audio_note, self)
        self.extract_audio_note_label.setGeometry(20, 220, 580, 40)
        self.extract_audio_note_label.setAlignment(QtCore.Qt.AlignLeft)
        self.extract_audio_note_label.setStyleSheet("color: white;")

        self.btn_extract = QPushButton("Extract Audio", self)
        self.btn_extract.setGeometry(240, 140 + self.btn_hide.height() + button_spacing, 120, 40)
        self.btn_extract.clicked.connect(self.extract_audio)

        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

    def hide_audio(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Select Image to Hide Audio", "", "Image Files (*.png *.jpg *.jpeg)")
        audio_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File to Hide", "", "Audio Files (*.wav *.mp3)")

        if image_path and audio_path:
            stegano_path = os.path.splitext(image_path)[0] + "_stegano.png"

            image = Image.open(image_path)
            audio_data = open(audio_path, 'rb').read()

            # Hide audio data within the image using LSB technique
            stegano_image = self.hide_audio_in_image(image, audio_data)

            stegano_image.save(stegano_path)

            # Set the message label
            self.label.setText("Audio hidden successfully in the image.")
            self.display_message("Encryption Complete", "Audio encrypted successfully!\nand saved in currunt directory ")

    def hide_audio_in_image(self, image, audio_data):
        # Convert audio data to binary
        audio_binary = ''.join(format(byte, '08b') for byte in audio_data)

        # Iterate through image pixels and hide audio data in LSBs
        index = 0
        for y in range(image.height):
            for x in range(image.width):
                r, g, b = image.getpixel((x, y))
                if index < len(audio_binary):
                    r = int(format(r, '08b')[:-1] + audio_binary[index], 2)
                    index += 1
                if index < len(audio_binary):
                    g = int(format(g, '08b')[:-1] + audio_binary[index], 2)
                    index += 1
                if index < len(audio_binary):
                    b = int(format(b, '08b')[:-1] + audio_binary[index], 2)
                    index += 1
                new_pixel = (r, g, b)
                image.putpixel((x, y), new_pixel)

                if index >= len(audio_binary):
                    break
            if index >= len(audio_binary):
                break

        return image

    def extract_audio(self):
        stegano_path, _ = QFileDialog.getOpenFileName(self, "Select Steganographic Image", "", "Image Files (*.png *.jpg *.jpeg)")

        if stegano_path:
            output_audio_path = os.path.splitext(stegano_path)[0] + "_extracted.wav"

            stegano_image = Image.open(stegano_path)

            extracted_audio_data = self.extract_audio_from_image(stegano_image)

            with open(output_audio_path, "wb") as audio_file:
                audio_file.write(extracted_audio_data)

            # Set the message label
            self.label.setText("Audio extracted successfully.")
            self.display_message("Decryption Complete", "Audio decrypted successfully!\nand stored in.wav extention ")

    def extract_audio_from_image(self, image):
        audio_binary = ''
        for pixel in image.getdata():
            r, g, b = pixel
            audio_binary += format(r, '08b')[-1]
            audio_binary += format(g, '08b')[-1]
            audio_binary += format(b, '08b')[-1]

        extracted_audio_data = bytearray()
        for i in range(0, len(audio_binary), 8):
            byte = audio_binary[i:i+8]
            extracted_audio_data.append(int(byte, 2))

        return extracted_audio_data



# Define the Login class with DB connection
# class Login(QtWidgets.QDialog):
#     def __init__(self):
#         super(Login, self).__init__()
#         loadUi(os.path.abspath("login.ui"), self)
#         self.loginbutton.clicked.connect(self.loginfunction)
#         self.password.setEchoMode(QtWidgets.QLineEdit.Password)
#         self.setStyleSheet("background-image: url(img.jpg);")
#         self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
#         self.conn = mysql.connector.connect(
#             host="localhost",
#             port="3308",
#             user="root",
#             password="root",
#             database="login"
#         )
#         self.cursor = self.conn.cursor(buffered=True)

#     def close_database(self):
#         if self.cursor:
#             self.cursor.close()
#         if self.conn.is_connected():
#             self.conn.close()

#     def __del__(self):
#         self.close_database()

#     def loginfunction(self):
#         email = self.email.text()
#         password = self.password.text()

#         try:
#             query = "SELECT * FROM users WHERE email=%s AND password=%s"
#             self.cursor.execute(query, (email, password))
#             user = self.cursor.fetchone()

#             if user:
#                 print("Successfully logged in with email:", email)
#                 self.close_database()  # Close the database connection
#                 self.close()  # Close the login window
#                 self.page_after_login = PageAfterLogin()
#                 self.page_after_login.show()  # Show the page after login
#             else:
#                 print("Login failed. Invalid credentials.")
#         except mysql.connector.Error as err:
#             print("Error:", err)

# without DB connection
class Login(QtWidgets.QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi(os.path.abspath("login.ui"), self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.setStyleSheet("background-image: url(img.jpg);")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)

    def loginfunction(self):
        # Define default username and password for authentication
        default_username = "user"
        default_password = "1234"

        entered_username = self.email.text()
        entered_password = self.password.text()

        if entered_username == default_username and entered_password == default_password:
            print("Successfully logged in with username:", entered_username)
            self.close()  # Close the login window
            self.page_after_login = PageAfterLogin()
            self.page_after_login.show()  # Show the page after login
        else:
            # Show an "Invalid credentials" message
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Invalid credentials")
            msg.setWindowTitle("Login Failed")
            msg.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_window = Login()

    # Show the login window
    login_window.show()

    sys.exit(app.exec_())
