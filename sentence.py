#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt4 import QtCore, QtSql
from subprocess import check_output

parser = "tatoparser"
show_id = "--display-ids"
show_lang = "--display-lang"

class Sentence(QtCore.QThread):
    def __init__(self, ddict):
        super(Sentence, self).__init__()
        self.dict = ddict

    def run(self):
        st = self.getSentence()
        self.emit(QtCore.SIGNAL("output(PyQt_PyObject)"), st)

    def getSentence(self):
        print self.dict
        key = self.dict.keys()[-1]
        value = self.dict[key]
        sentence = unicode(
            check_output([parser, show_id, show_lang, key, value]),
            'utf-8').rstrip("\n")
        print "in Sentence",sentence
        return sentence
        
def getTranslationById(id):
    sentences = unicode(
        check_output([parser, show_id, show_lang, "--is-linked-to", str(id)]), 
        'utf-8').rstrip("\n")
    return sentences

# support filters 
def getSentencesByRegex(regex):
    regexUTF8 = regex.toUtf8()
    regexUTF8 = ".*" + regexUTF8 + ".*"
    sentences = unicode(
        check_output([parser, show_id, show_lang, "-r", str(regexUTF8)]),
        'utf-8').rstrip("\n")
    return sentences

def insertRecord(self, sentence, model, row, isTr, listid):
    try:
        iid, lang, st = sentence.split("\t")
        record = QtSql.QSqlRecord()
        f0 = QtSql.QSqlField("stid", QtCore.QVariant.Int)
        f1 = QtSql.QSqlField("tatoid", QtCore.QVariant.Int)
        f2 = QtSql.QSqlField("listid", QtCore.QVariant.Int)
        f3 = QtSql.QSqlField("sentence", QtCore.QVariant.String)
        f4 = QtSql.QSqlField("lang", QtCore.QVariant.String)
        f5 = QtSql.QSqlField("sortid", QtCore.QVariant.Int)
        f6 = QtSql.QSqlField("tr", QtCore.QVariant.String)
        f0.clear()
        f1.setValue(QtCore.QVariant(iid))
        f2.setValue(QtCore.QVariant(listid))
        f3.setValue(QtCore.QVariant(st))
        f4.setValue(QtCore.QVariant(lang))
        if row == -1:
            f5.setValue(QtCore.QVariant(model.rowCount()*10))
        else:
            f5.setValue(QtCore.QVariant(row*10+1))
        f6.setValue(QtCore.QVariant(isTr))
        record.append(f0)
        record.append(f1)
        record.append(f2)
        record.append(f3)
        record.append(f4)
        record.append(f5)
        record.append(f6)
        model.insertRecord(-1, record)
    except ValueError:
        print "an invalid sentence, we ignore it"
