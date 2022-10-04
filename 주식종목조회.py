import time

import win32com.client
import constant.MyAccount
import pythoncom


class XASession:
    IsLogin = False

    def OnLogin(self, code, message):
        print("로그인성공 code = %s" % code)
        XASession.IsLogin = True


class XAQuery:
    T8430_event = None
    T8430_IsSuccess = False

    def OnReceiveData(self, code):
        print(code)
        if code == 't8430':
            count = XAQuery.T8430_event.GetBlockCount("t8430OutBlock")
            for i in range(count):
                종목명 = XAQuery.T8430_event.GetFieldData("t8430OutBlock", "hname", i)
                기준가 = XAQuery.T8430_event.GetFieldData("t8430OutBlock", "recprice", i)

                if XAQuery.T8430_event.GetFieldData("t8430OutBlock", "gubun", i) == '1':
                    기준 = "코스피"
                else:
                    기준 = "코스닥"

                print("시장 = %s %s 종목명 = %s, 기준가 = %s" % (기준, i, 종목명, 기준가))

            XAQuery.T8430_IsSuccess = True


class Main:
    # t8430
    def __init__(self):
        session = win32com.client.DispatchWithEvents("XA_Session.XASession", XASession)
        session.ConnectServer(constant.MyAccount.PRD_SERVER_URL, constant.MyAccount.PRD_PORT)

        if session.IsConnected( ) is True:
            session.Login(constant.MyAccount.ID, constant.MyAccount.PASSWORD, constant.MyAccount.ENC_PASSWORD, 0, False)

            while session.IsLogin is False:
                pythoncom.PumpWaitingMessages( )

            XAQuery.T8430_event = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQuery)
            XAQuery.T8430_event.ResFileName = "/Res/t8430.res"
            
            Main.t8430_주식종목조회(gubun="1", IsNext=False)
            Main.t8430_주식종목조회(gubun="2", IsNext=False)

        else:
            session.DisconnectServer( )

    @staticmethod
    def t8430_주식종목조회(gubun=None, IsNext=False):
        time.sleep(0.51)

        XAQuery.T8430_event.SetFieldData("t8430InBlock", "gubun", 0, gubun)
        XAQuery.T8430_event.Request(IsNext)

        XAQuery.T8430_IsSuccess = False
        while XAQuery.T8430_IsSuccess is False:
            pythoncom.PumpWaitingMessages( )


if __name__ == '__main__':
    Main( )
