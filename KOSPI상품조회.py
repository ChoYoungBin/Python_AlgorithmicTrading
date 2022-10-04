from 로그인2 import LogIn as Login
import win32com.client
import pythoncom


class XAQuery:
    isDataReceived = False

    def OnReceiveData(self, tr_code):
        XAQuery.isDataReceived = True
        print(tr_code)
        print(self.GetFieldData("t1101OutBlock", "hname", 0))


class XQuery_t1101:

    def getSingleData(self, code):
        XQuery_t1101 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQuery)
        XQuery_t1101.ResFileName = "/Res/t1101.res"
        XQuery_t1101.SetFieldData("t1101InBlock", "shcode", 0, code)

        XQuery_t1101.Request(False)
        while XQuery_t1101.isDataReceived is False:
            pythoncom.PumpWaitingMessages( )


if __name__ == '__main__':
    loginObj = Login( )
    session = loginObj.logIn( )

    mainObj = XQuery_t1101( )
    mainObj.getSingleData("005930")
