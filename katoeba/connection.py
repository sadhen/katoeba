from PyQt4 import QtSql, QtGui
import sys
import os
import sentence as st

class Data(object):
    def __init__(self):
        if self.createConnection() == False:
            sys.exit(1)
        self.query = QtSql.QSqlQuery()
        self.query.exec_("PRAGMA page_size = 4096");
        self.query.exec_("PRAGMA cache_size = 16384")
        self.query.exec_("PRAGMA temp_store = MEMORY");
        self.query.exec_("PRAGMA journal_mode = OFF");
        self.query.exec_("PRAGMA locking_mode = EXCLUSIVE");
        self.query.exec_("PRAGMA synchronous = OFF");

        if self.db.tables().isEmpty():
            self.query.exec_("create table list "
                             "(id integer primary key autoincrement NOT NULL UNIQUE,"
                             "name varchar(256),"
                             "number int)")
            self.query.exec_("insert into list (name, number) values('Temp', 0)")
            self.query.exec_("create table sentences "
                             "(stid integer primary key autoincrement NOT NULL UNIQUE, "
                             "tr varchar(3),"
                             "listid int,"
                             "sentence varchar(256),"
                             "lang varchar(3),"
                             "sortid int,"
                             "tatoid int)"
                             )

    def createConnection(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(os.path.expanduser("~/.config/katoeba/tatoeba.db"))
        if not self.db.open():
            QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
                                       QtGui.qApp.tr("Unable to establish a database connection.\n"
                                                     "This example needs SQLite support. Please read "
                                                     "the Qt SQL driver documentation for information "
                                                     "how to build it.\n\n"
                                                     "Click Cancel to exit."),
                                       QtGui.QMessageBox.Cancel)
            return False
        return True
