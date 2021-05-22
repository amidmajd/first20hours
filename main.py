import sys
import time
import os
from PyQt5 import QtGui, QtWidgets, QtCore
from gmain import Ui_MWindow as main_ui
import sqlite3 as sql


class Main:
    def __init__(self):
        self.ui = main_ui()
        self.window = QtWidgets.QMainWindow()
        self.ui.setupUi(self.window)
        self.window.setFixedSize(self.window.size())
        self.window.closeEvent = self.closeEvent

        self.conn = sql.connect('first-20-hours.sqlite')
        self.c = self.conn.cursor()
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        if self.c.fetchall() == []:
            self.c.execute('CREATE TABLE hours (task_name TEXT, task_h REAL, task_active INTEGER)')
            for i in range(4):
                self.c.execute('INSERT INTO hours VALUES(NULL, 0, 0)')
            self.conn.commit()

        self.a_data = [list(x) for x in self.c.execute('SELECT * FROM hours').fetchall()]
        # print(self.a_data)

        self.initialization()

        self.ui.act_task_1.stateChanged.connect(self.task_activator)
        self.ui.act_task_2.stateChanged.connect(self.task_activator)
        self.ui.act_task_3.stateChanged.connect(self.task_activator)
        self.ui.act_task_4.stateChanged.connect(self.task_activator)

        self.ui.edit_task_name_1.stateChanged.connect(self.task_name_edit)
        self.ui.edit_task_name_2.stateChanged.connect(self.task_name_edit)
        self.ui.edit_task_name_3.stateChanged.connect(self.task_name_edit)
        self.ui.edit_task_name_4.stateChanged.connect(self.task_name_edit)

        self.ui.delete_task_1.clicked.connect(self.task_delete)
        self.ui.delete_task_2.clicked.connect(self.task_delete)
        self.ui.delete_task_3.clicked.connect(self.task_delete)
        self.ui.delete_task_4.clicked.connect(self.task_delete)

        self.ui.add_new_time_1.clicked.connect(self.task_add_time)
        self.ui.add_new_time_2.clicked.connect(self.task_add_time)
        self.ui.add_new_time_3.clicked.connect(self.task_add_time)
        self.ui.add_new_time_4.clicked.connect(self.task_add_time)

    def initialization(self):
        for i in range(4):
            if self.a_data[i][-1] == 1:

                exec('self.ui.task_frame_{}.setEnabled(True)'.format(i+1))
                exec('self.ui.task_name_{}.setEnabled(True)'.format(i+1))
                exec('self.ui.act_task_{}.setEnabled(False)'.format(i+1))
                exec('self.ui.act_task_{}.setChecked(True)'.format(i+1))

                exec('self.ui.task_name_{}.setText("{}")'.format(i+1, self.a_data[i][0]))

                exec('self.ui.task_passed_h_{}.setText("{}")'.format(i+1, self.a_data[i][1]))
                exec('self.ui.task_rem_h_{}.setText("{}")'.format(i+1, 20 - self.a_data[i][1]))
                exec('self.ui.progressBar_{}.setValue({})'.format(i+1, (self.a_data[i][1] / 20)*100))

    def task_activator(self, s):
        sender = self.window.sender()
        sender.setEnabled(False)
        sender_n = int(sender.objectName()[-1])
        exec('self.ui.task_frame_{}.setEnabled(True)'.format(sender_n))
        exec('self.ui.task_name_{}.setEnabled(True)'.format(sender_n))
        self.a_data[sender_n-1][-1] = 1

    def task_name_edit(self, s):
        sender_n = int(self.window.sender().objectName()[-1])
        if s == 2:
            exec('self.ui.task_name_{}.setReadOnly(False)'.format(sender_n))
        else:
            exec('self.ui.task_name_{}.setReadOnly(True)'.format(sender_n))
            t_name = eval('self.ui.task_name_{}.text()'.format(sender_n))
            self.a_data[sender_n-1][0] = t_name.rstrip()

    def task_delete(self):
        tmp_message_box = QtWidgets.QMessageBox.question(self.window,
                                                         'Deleting Selected Task!',
                                                         'Selected Task will be deleted...    Are you Sure?',
                                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if tmp_message_box == QtWidgets.QMessageBox.No:
            return

        sender_n = int(self.window.sender().objectName()[-1])
        exec('self.ui.task_name_{}.setText("")'.format(sender_n))
        exec('self.ui.progressBar_{}.setValue(0)'.format(sender_n))
        exec('self.ui.task_passed_h_{}.setText("0")'.format(sender_n))
        exec('self.ui.task_rem_h_{}.setText("0")'.format(sender_n))
        exec('self.ui.new_time_{}.setValue(0)'.format(sender_n))
        exec('self.ui.act_task_{}.setChecked(False)'.format(sender_n))
        exec('self.ui.act_task_{}.setEnabled(True)'.format(sender_n))
        exec('self.ui.task_frame_{}.setEnabled(False)'.format(sender_n))
        self.a_data[sender_n-1] = [None, 0, 0]

    def task_add_time(self):
        sender_n = int(self.window.sender().objectName()[-1])
        minutes = int(eval('self.ui.new_time_{}.value()'.format(sender_n)))
        temp_h = round(minutes / 60, 2)

        # check for compelete task
        if temp_h + self.a_data[sender_n-1][1] >= 20:
            tmp_message_box = QtWidgets.QMessageBox.warning(self.window,
                                                            'Task Completed!',
                                                            'Well Done :)   You achieved 20 hours in this Task...')

        self.a_data[sender_n-1][1] += temp_h

        exec('self.ui.new_time_{}.setValue(0)'.format(sender_n))
        exec('self.ui.task_passed_h_{}.setText("{}")'.format(sender_n, self.a_data[sender_n-1][1]))
        exec('self.ui.task_rem_h_{}.setText("{}")'.format(sender_n, 20 - self.a_data[sender_n-1][1]))
        exec('self.ui.progressBar_{}.setValue({})'.format(sender_n, (self.a_data[sender_n-1][1] / 20)*100))

    def install_fonts(self):
        f = QtGui.QFontDatabase()
        f.addApplicationFont("GE_Inspira.ttf")

    def closeEvent(self, event):
        # print('\nclose',self.a_data)

        for i in range(4):
            if self.a_data[i][0] == None:
                self.a_data[i][-1] = 0

        n = [x[0] for x in self.a_data]
        h = [x[1] for x in self.a_data]
        a = [x[2] for x in self.a_data]

        for i in range(4):
            self.c.execute('UPDATE hours SET task_name = ? , task_h = ? , task_active = ? WHERE _rowid_ = ?', [
                           n[i], h[i], a[i], i+1])

        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('plastique'))
    screen_resolution = app.desktop().screenGeometry()
    screen_size = screen_resolution.width(), screen_resolution.height()

    M = Main()
    M.window.move((screen_size[0] - M.window.width())//2, (screen_size[1] - M.window.height())//2 - 30)
    M.window.show()
    sys.exit(app.exec_())
