# Form implementation generated from reading ui file 'C:\Users\Maks\PycharmProjects\PythonProject3\get_client_ui.ui'
#
# Created by: PyQt6 UI code generator 6.9.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class ClientUi(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(587, 464)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = ClientUi()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
