
# coding: utf-8

# # GUI Import

# In[1]:


import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QApplication, QListWidget, QPushButton, QRadioButton, QPlainTextEdit)


# # Core Import
# User Pass: uT!ZRIyy!KBu

# In[2]:


import sqlite3
import json
import ast
import psycopg2
import base64


# # Core Class

# In[3]:


class DataBase:
    """
    SQL DATABASE
    """
    def __init__(self):
        self.proparty = ["IC_NO", "UNIT", "PINS", "DISC", "DIMENSION", "INPUT", "OUTPUT", "TYPE", "PACKAGE", "TRUTH_TABLE", "OPERATION"]
        self.__open()
        
    def __del__(self):
        self.__close()
        
    def __close(self):
        self.__conn.close()
        
    def __open(self):
        db_username = 'kehnpahh'
        db_password = 'sJHgHTMcTwA72WbeC9280rnlbbZLyrug'
        db_host = 'tantor.db.elephantsql.com'
        db_port = 5432
        db_database = 'kehnpahh'
        self.__conn = psycopg2.connect(database=db_database, 
                                       user= db_username, 
                                       password=db_password,
                                       host=db_host,
                                       port=db_port)
    def encode(self, string):
        encoded = base64.b64encode(bytes(string, "utf-8"))
        tmp_enc = encoded.decode('utf-8').replace("=", "^")
        enc = ""
        for c in tmp_enc:
            enc += (chr(ord(c)+1))
        return enc
    def decode(self, string):
        dec = ""
        for c in string.replace("_", ">"):
            dec += (chr(ord(c)-1))
        data = base64.b64decode(dec)
        return data.decode('utf-8')
        
    def create(self):
        try:
            cur = self.__conn.cursor()
            cur.execute('''CREATE TABLE NONAME
                     (IC_NO CHAR(100) PRIMARY KEY     NOT NULL,
                     UNIT           TEXT    NOT NULL,
                     PINS            TEXT     NOT NULL,
                     DISC            TEXT     NOT NULL,
                     DIMENSION           TEXT    NOT NULL,
                     INPUT           TEXT    NOT NULL,
                     OUTPUT           TEXT    NOT NULL,
                     TYPE           TEXT    NOT NULL,
                     PACKAGE           TEXT    NOT NULL,
                     TRUTH_TABLE           TEXT    NOT NULL,
                     OPERATION           TEXT    NOT NULL);''')
            cur.close()
            self.__conn.commit()
            return True
        except Exception as e:
            print("create(): "+str(e))
            return False
        
    def upload(self):
        try:
            f = open("74XX Serise.txt", 'r')
            d = f.read()
            cur = self.__conn.cursor()
            for line in d.split('\n'):
                info = line.split('\t')
                print(info[0])
                cur.execute("INSERT INTO NONAME (IC_NO ,UNIT,PINS,DISC,DIMENSION, INPUT, OUTPUT, TYPE, PACKAGE, TRUTH_TABLE, OPERATION)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )", (self.encode(info[0]) , self.encode(info[1]) , self.encode(info[2]) , self.encode(info[3]), self.encode(info[4]), self.encode(info[5]), self.encode(info[6]), self.encode(info[7]), self.encode(info[8]), self.encode('{"head": {"no_of_input": 0,"no_of_output": 0}, "inputs": {"line1": []},"outputs": {"line1": []}}'), self.encode("NA")));
            cur.close()
            self.__conn.commit()
            f.close()
            return True
        except Exception as e:
            print("upload() :"+str(e))
            return False
    def show(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT * from NONAME")
        i = 0
        while True:
            row = cur.fetchone()
            if row == None:
                break
            if row[7] != "NA":
                i+=1
            print(i)
        cur.close()
        self.__conn.commit()
    
    def get(self, id):
        cur = self.__conn.cursor()
        id = self.encode(id)
        cur.execute("SELECT * from NONAME WHERE IC_NO = '"+str(id)+"'")
        d = []
        while True:
            row = cur.fetchone()
            if row == None:
                break
            tmp = []
            for item in row:
                tmp.append(self.decode(item))
            d = tmp.copy()
        cur.close()
        self.__conn.commit()
        return d
    
    def getAll(self):
        cur = self.__conn.cursor()
        cur.execute("SELECT IC_NO from NONAME")
        d = []
        while True:
            row = cur.fetchone()
            if row == None:
                break
            tmp = []
            for item in row:
                d.append(self.decode(item))
        cur.close()
        self.__conn.commit()
        d.sort()
        return d
        
        
    def update(self):
        print("[.] to accept\n[Enter] to skip\n")
        f = open("update.ic", 'r')
        d = f.read()
        i = 1
        for line in d.split('\n'):
            if line:
                print(str(i)+". -----------------------------\n")
                i+=1
                info = line.split('\t')
                ic_info = self.get(info[0])
                print(ic_info)
                print(info[1]+" : "+ ic_info[self.proparty.index(info[1])] +" --> "+ info[2])
                ans = input()
                if ans == ".":
                    cur = self.__conn.cursor()
                    cur.execute("UPDATE NONAME set "+str(info[1])+" = '"+self.encode(str(info[2]))+"' where IC_NO = '"+self.encode(str(info[0]))+"'")
                    cur.close()
                    self.__conn.commit()
                    print("Done.\n")
        
    def request_update(self, id, field, value):
        if field in self.proparty:
            f = open("update.ic", 'a')
            f.write(str(id) + '\t'+str(field)+'\t'+value+'\tNO\n')
            f.close()
            return True
        else:
            return None
        
    def toCSV(self, file):
        f = open(file, 'w+')
        f.write("IC_NO ,UNIT,PINS,DISC,DIMENSION, INPUT, OUTPUT, TYPE, PACKAGE, TRUTH_TABLE, OPERATION\n")
        cursor = self.__conn.execute("SELECT * from NONAME")
        for row in cursor:
            for item in row:
                if ',' in str(item):
                    f.write('"'+str(item)+'"')
                else:
                    f.write(str(item))                    
                f.write(',')
            f.write('\n')
        cursor.close()
        self.__conn.commit()
        f.close()
        
    def save(self, file):
        f = open(file, 'w+')
        cur = self.__conn.cursor()
        cur.execute("SELECT * from NONAME")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            for item in row:
                f.write(str(item))                    
                f.write('\t')
            f.write('\n')
        cur.close()
        self.__conn.commit()
        f.close()


# # GUI Class

# In[4]:


class GUI(QWidget):
    """
    **GUI Class for first window**
    """
    def __init__(self):
        super().__init__()
        self.db = DataBase()
        self.initUI()
        
    def setICDetails(self, selection, j):
        seen = set()
        indexes = []
        model = self.list.model()
        self.info.clear()
        for index in selection.indexes():
            if index.row() not in seen:
                ic_no = self.ics[index.row()]
                IC_NO ,UNIT,PINS,DISC,DIMENSION, INPUT, OUTPUT, TYPE, PACKAGE, TRUTH_TABLE, OPERATION = self.db.get(ic_no)
                self.edit_id.setText(IC_NO)
                self.info.addItem("IC_NO\t: "+str(IC_NO))
                self.info.addItem("UNIT\t: "+str(UNIT))
                self.info.addItem("PINS\t: "+str(PINS))
                self.info.addItem("DISC\t: "+str(DISC))
                self.info.addItem("DIMENSION\t: "+str(DIMENSION))
                self.info.addItem("INPUT\t: "+str(INPUT))
                self.info.addItem("OUTPUT\t: "+str(OUTPUT))
                self.info.addItem("TYPE\t: "+str(TYPE))
                self.info.addItem("PACKAGE\t: "+str(PACKAGE))
                self.info.addItem("OPERATION\t: "+str(OPERATION))
                val = ast.literal_eval(TRUTH_TABLE)
                json_data = json.loads(json.dumps(val))

                no_ip = int(json_data['head']["no_of_input"])
                no_op = int(json_data['head']["no_of_output"])
                inputs = json_data['inputs']
                output = json_data['outputs']
                self.truthTable.clear()
                for in_line, out_line in zip(inputs, output):
                    self.truthTable.insertPlainText(str(inputs[in_line]) + '\t' +str(output[out_line])+"\n")
                
    def setField(self, selection, j):
        seen = set()
        indexes = []
        model = self.info.model()
        proparty = ["IC_NO", "UNIT", "PINS", "DISC", "DIMENSION", "INPUT", "OUTPUT", "TYPE", "PACKAGE", "OPERATION"]
        for index in selection.indexes():
            if index.row() not in seen:
                self.edit_prop.setText(proparty[index.row()])
        
    def save_clicked(self):
        id = str(self.edit_id.text())
        prop = str(self.edit_prop.text())
        value = str(self.edit_value.text())
        self.db.request_update(id, prop, value)
        self.edit_id.setText("")
        self.edit_prop.setText("")
        self.edit_value.setText("")
        
    def initUI(self):
        self.appname = QLabel("List of 74XX IC", self)
        self.save = QPushButton("Save", self)
        self.edit_id = QLineEdit("IC No", self)
        self.edit_prop = QLineEdit("Field", self)
        self.edit_value = QLineEdit("New Value", self)
        self.truthTable = QPlainTextEdit("False", self)
        
        self.list = QListWidget(self)
        self.info = QListWidget(self)
        self.ics = self.db.getAll()
        
        # List
        for ic in self.ics:
            self.list.addItem(str(ic))
        self.list.show()

        self.save.clicked.connect(self.save_clicked)
        self.list.setSelectionMode(1)
        self.list.selectionModel().selectionChanged.connect(self.setICDetails)
        self.info.selectionModel().selectionChanged.connect(self.setField)
        
        self.save.move(400, 150)
        self.appname.move(120, 10)
        self.list.move(40, 30)
        self.info.move(120, 30)
        self.edit_id.move(400, 60)
        self.edit_prop.move(400, 90)
        self.edit_value.move(400, 120)
        self.truthTable.move(40, 240)
        
        self.truthTable.resize(550, 100)
        
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('74XX IC')
        self.show()


# # Main

# In[5]:


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = GUI()
    app.exec_()
    exit()

