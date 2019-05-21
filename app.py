# -*- coding: utf-8 -*- 
import sys, time
from PySide.QtCore import *
from PySide.QtGui import *
import requests
import json
import threading
from datetime import datetime

FILE_POINTER = None
DATA_API_THREAD = None
DATA_MEAS_TIME = 1

def startData():
    global DATA_API_THREAD
    global FILE_POINTER
    # ファイルをオープン
    strFile = datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv"
    FILE_POINTER = open(strFile, 'w')

    # スレッド開始
    DATA_API_THREAD = DataApiThread()
    DATA_API_THREAD.start()

def stopData():
    # スレッド停止
    global DATA_API_THREAD
    global FILE_POINTER
    if DATA_API_THREAD != None:
        DATA_API_THREAD.stop()
        DATA_API_THREAD = None
    # ファイルを閉じる
    if FILE_POINTER != None:
        FILE_POINTER.close()
        FILE_POINTER = None

class DataApiThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ExecFlg = True

    def run(self):
        global FILE_POINTER
        self.ExecFlg = True

        while 1:
            if self.ExecFlg == False:
                break
            strRet = self.getDataApi()
            if FILE_POINTER != None:
                FILE_POINTER.write(strRet + '\n')
            time.sleep(DATA_MEAS_TIME)

    def stop(self):
        self.ExecFlg = False

    def getDataApi(self):
        url = 'https://api.particle.io/v1/devices/2d0044001047343438323536/data'
        params = dict(
            access_token='486a334496fc16fbdf74e11ade7f67b44b2fa467'
        )

        resp = requests.get(url=url, params=params)
        objResponse = json.loads(resp.text)

        return objResponse['result']

class MyMainDialog(QDialog):
    # ウィンドウの初期化処理
    def __init__(self, parent=None):
        # ベース・クラスの初期化
        super(MyMainDialog, self).__init__(parent)

        # ウィンドウタイトルを設定
        self.setWindowTitle(u"Particleデータ出力")

        # ダイアログサイズ設定
        self.resize(300, 200)

        self.myButton = QPushButton(u"測定開始", self)
        self.myButton.move(50, 50)
        self.myButton.resize(200, 100)

        # ボタンが押された時の処理を設定
        self.myButton.clicked.connect(self.myButtonClicked)


    # ボタンが押された時の処理
    def myButtonClicked(self):
        if self.myButton.text() == u"測定開始":
            startData()
            self.myButton.setText(u"停止")
        else:
            stopData()
            self.myButton.setText(u"測定開始")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MyMainDialog()
    mainWin.show()
    sys.exit(app.exec_())
