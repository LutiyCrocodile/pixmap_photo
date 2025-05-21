from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QByteArray
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QByteArray
from GUI import *
import MySQLdb as mdb
import os

if not os.path.exists("save_img"):
    os.makedirs("save_img")

conn = mdb.connect(host="localhost", user="root", password="", database="pixmap")


def get_data() -> list:
    cursor = conn.cursor()
    cursor.execute("SELECT name, photo FROM books")
    return cursor.fetchall()


class MainWin(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.setupUi(self)
        res_data = get_data()
        height = 20

        for record in res_data:
            book_name, photo_blob = record

            byte_array = QByteArray(photo_blob)

            qimage = QImage.fromData(byte_array)

            if qimage.isNull():
                print(f"Ошибка загрузки изображения для записи {book_name}")
                continue

            qpixmap = QPixmap.fromImage(qimage)
            file_path = f"save_img/{book_name}.jpg"
            qpixmap.save(file_path, "JPG")

            lb = QtWidgets.QLabel(self)
            lb.setGeometry(QtCore.QRect(10, height, 170, 170))
            lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lb.setText(f"{record[0]} \n {record[1]}")
            lb.setObjectName(f"{record[0]}")
            lb.setPixmap(qpixmap.scaled(170, 170))

            lb_t = QtWidgets.QLabel(self)
            lb_t.setGeometry(QtCore.QRect(200, height, 210, 150))
            lb_t.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lb_t.setText(f"{record[0]}")
            lb_t.setObjectName(f"{record[0]}")

            height += 180


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wind = MainWin()
    wind.show()
    sys.exit(app.exec())
