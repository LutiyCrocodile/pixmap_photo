from itertools import count

from PyQt6 import QtWidgets
from get_client_ui import *
from PyQt6.QtCore import Qt, QByteArray
from PyQt6.QtGui import QImage, QPixmap, QFont
from PyQt6.QtCore import QByteArray
from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel

from GUI import *
import MySQLdb as mdb
import os

if not os.path.exists("save_img"):
    os.makedirs("save_img")

conn = mdb.connect(host="localhost", user="root", password="", database="pixmap")


def get_data() -> list:
    cursor = conn.cursor()
    cursor.execute(f"CALL all_info();")
    return cursor.fetchall()


class MainWin(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.setupUi(self)
        res_data = get_data()
        app.setStyleSheet("QLabel{font-size: 14pt;}")
        height = 20

        self.lbl_name = QtWidgets.QLabel(self)
        self.lbl_name.setGeometry(QtCore.QRect(250, 10, 300, 80))
        self.lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_name.setText("Книжный магазин")



        for record in res_data:
            email, phone, id_client, num_of_books, total = record

            # byte_array = QByteArray(photo_blob)

            # qimage = QImage.fromData(byte_array)

            # if qimage.isNull():
            #     print(f"Ошибка загрузки изображения для записи {name}")
            #     continue

            # qpixmap = QPixmap.fromImage(qimage)
            # file_path = f"save_img/{name}.jpg"
            # qpixmap.save(file_path, "JPG")

            # lb = QtWidgets.QLabel(self)
            # lb.setGeometry(QtCore.QRect(10, 200, 170, 170))
            # lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # lb.setText(f"{photo_blob}")
            # lb.setObjectName(f"{name}")
            # lb.setPixmap(qpixmap.scaled(170, 170))

            self.lb_t = QtWidgets.QLabel(self)
            self.lb_t.setGeometry(QtCore.QRect(40, 100 + height, 800, 300))
            self.lb_t.setAlignment(Qt.AlignmentFlag.AlignLeft),
            self.lb_t.setText(f"{id_client}, {phone},  {email},  {num_of_books}, {total}")


            height += 80
        self.input_client_id = QLineEdit(self)
        self.input_client_id.setGeometry(QtCore.QRect(250, 450, 300, 40))
        self.input_client_id.setStyleSheet("background: #df")
        self.input_client_id.setPlaceholderText("Введите id клиента")
        self.input_client_id.setInputMask("000")
        self.input_client_id.setText("0")

        self.btn_get_client = QtWidgets.QPushButton(self)
        self.btn_get_client.setGeometry(QtCore.QRect(300, 500, 200, 40))
        self.btn_get_client.setText("Найти")
        self.btn_get_client.clicked.connect(self.get_client)

    def get_client(self):
        self.client = ClientUi(self.input_client_id.text())
        self.client.show()
        self.close()




class ClientUi(QtWidgets.QWidget, ClientUi):
    def __init__(self, id_client, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.id_client = id_client

        height = 70

        conn = mdb.connect(host="localhost", user="root", password="", database="pixmap")
        cursor = conn.cursor()
        cursor.execute(f"CALL book_for_client({self.id_client});")
        res = cursor.fetchall()
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(260, 20, 300, 30))
        self.label.setObjectName("label")
        self.label.setText(f"Клиент {id_client}")
        for record in res:
            photo, name, date_of_purchase, quantity = record

            byte_array = QByteArray(photo)

            qimage = QImage.fromData(byte_array)

            if qimage.isNull():
                print(f"Ошибка загрузки изображения для записи {name}")
                continue

            qpixmap = QPixmap.fromImage(qimage)
            file_path = f"save_img/{name}.jpg"
            qpixmap.save(file_path, "JPG")

            lb = QtWidgets.QLabel(self)
            lb.setGeometry(QtCore.QRect(10, height, 170, 170))
            lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lb.setText(f"{photo}")
            lb.setObjectName(f"{name}")
            lb.setPixmap(qpixmap.scaled(170, 170))

            lb_text = QtWidgets.QLabel(self)
            lb_text.setStyleSheet("text-size: 10px")
            lb_text.setGeometry(QtCore.QRect(180, height, 800, 300))
            lb_text.setAlignment(Qt.AlignmentFlag.AlignLeft),
            lb_text.setText(f"Название: {name},\n Дата покупки: {date_of_purchase},\n  Количество: {quantity}")

            height += 180

        self.btn_back = QPushButton(self)
        self.btn_back.setGeometry(QtCore.QRect(300, 400, 200, 30))
        self.btn_back.setText("Назад")
        self.btn_back.clicked.connect(self.get_back)

    def get_back(self):
        self.back = MainWin()
        self.back.show()
        self.close()



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wind = MainWin()
    wind.show()
    sys.exit(app.exec())
