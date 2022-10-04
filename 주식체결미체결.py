import time

import win32com.client
import constant.MyAccount
import pythoncom

from Python_AlgorithmicTrading.constant import MyAccount


class XASession:
    IsLogin = False

    def OnLogin(self, code, message):
        print("code = %s" % code)
        XASession.IsLogin = True


class XAQuery:
    T0425_event = None
    T0425_IsSuccess = False

    def OnReceiveData(self, code):
        print(code)
        if code == 't0425':
            총주문수량 = self.T0425_event.GetFieldData("t0425OutBlock", "tqty", 0)
            주문번호 = self.T0425_event.GetFieldData("t0425OutBlock", "cts_ordno", 0)
            print('총 주문 수량은 = %s 개 입니다' % 총주문수량)
            출력숫자 = self.T0425_event.GetBlockCount("t0425OutBlock1")
            cts_ordno = self.T0425_event.GetFieldData("t0425OutBlock", "cts_ordno", 0)
            for index in range(출력숫자):
                self.T0425_event.GetFieldData("t0425OutBlock1", "ordno", index)

            print('출력1숫자 = %s 개 입니다' % 출력숫자)
            print("주문번호는 =%s" % 주문번호)

            if self.T0425_event.IsNext is True:
                주식체결미체결.T0425가져오기(IsNext=True, cts_ordno=cts_ordno)
            else:
                print("프로그램종료")
                XAQuery.T0425_IsSuccess = True


class 주식체결미체결:

    def start(self):
        session = win32com.client.DispatchWithEvents("XA_Session.XASession", XASession)
        session.ConnectServer(constant.MyAccount.PRD_SERVER_URL, constant.MyAccount.PRD_PORT)
        if session.IsConnected( ) is True:
            session.Login(constant.MyAccount.ID, constant.MyAccount.PASSWORD, constant.MyAccount.ENC_PASSWORD, 0, False)

            while XASession.IsLogin is False:
                pythoncom.PumpWaitingMessages( )

            주식체결미체결.T0425가져오기( )

        else:
            session.DisconnectServer( )

    @staticmethod
    def T0425가져오기(계좌번호: str = MyAccount.ACCOUNT_NUMBER, 비밀번호: str = MyAccount.ACCOUNT_PASSWORD, cts_ordno: str = "",
                  IsNext=False):
        time.sleep(0.1)

        XAQuery.T0425_event = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQuery)
        XAQuery.T0425_event.ResFileName = "/Res/t0425.res"
        XAQuery.T0425_event.SetFieldData("t0425InBlock", "accno", 0, 계좌번호)
        XAQuery.T0425_event.SetFieldData("t0425InBlock", "passwd", 0, 비밀번호)
        XAQuery.T0425_event.SetFieldData("t0425InBlock", "expcode", 0, "0")
        XAQuery.T0425_event.SetFieldData("t0425InBlock", "chegb", 0, "0")
        XAQuery.T0425_event.SetFieldData("t0425InBlock", "medosu", 0, "0")
        XAQuery.T0425_event.SetFieldData("t0425InBlock", "sortgb", 0, "1")
        XAQuery.T0425_event.SetFieldData("t0425InBlock", "cts_ordno", 0, cts_ordno)
        XAQuery.T0425_event.Request(IsNext)

        XAQuery.T0425_IsSuccess = False
        while XAQuery.T0425_IsSuccess is False:
            pythoncom.PumpWaitingMessages( )


if __name__ == '__main__':
    T0425obj = 주식체결미체결( )
    T0425obj.start( )
