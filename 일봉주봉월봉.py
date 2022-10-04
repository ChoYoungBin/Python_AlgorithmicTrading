import time

import pythoncom
import win32com.client

import constant.MyAccount


class XASession:
    IsLogin = False

    def OnLogin(self, code, message):
        print("로그인 성공 code = %s" % code)
        XASession.IsLogin = True


class XAQuery:
    t8413_event = None
    t8413_isOk = False

    rate_list = []

    def OnReceiveData(self, code):
        if code == 't8413':
            shcode = XAQuery.t8413_event.GetFieldData("t8413OutBlock", "shcode", 0)
            cts_date = XAQuery.t8413_event.GetFieldData("t8413OutBlock", "cts_date", 0)
            count = XAQuery.t8413_event.GetBlockCount("t8413OutBlock1")
            print("총갯수 = %s" % count)
            for i in range(count):
                # 현재부터 과거로 역순 조회
                i = count - i - 1
                date = XAQuery.t8413_event.GetFieldData("t8413OutBlock1", "date", i)
                close = XAQuery.t8413_event.GetFieldData("t8413OutBlock1", "close", i)
                rate = XAQuery.t8413_event.GetFieldData("t8413OutBlock1", "rate", i)

                convert_rate = float(rate)
                for ra in XAQuery.rate_list:
                    close = int(close) * (100 + ra) / 100
                    close = round(close)
                if convert_rate != 0.0:
                    XAQuery.rate_list.insert(0, convert_rate)

                print("일자 = %s , 수정종가 = %s, 수정주가비율 %s" % (date, close, rate))

            if self.IsNext is True:
                Main.t8413_주식차트일주월(shcode=shcode, gubun="3", qrycnt=500, sdate="", edate="99999999", cts_date=cts_date,
                                   comp_yn="N", IsNext=True)
            else:
                XAQuery.t8413_isOk = True


class Main:
    def __init__(self):
        session = win32com.client.DispatchWithEvents("XA_Session.XASession", XASession)
        session.ConnectServer(constant.MyAccount.PRD_SERVER_URL, constant.MyAccount.PRD_PORT)

        if session.IsConnected( ) is True:
            session.Login(constant.MyAccount.ID, constant.MyAccount.PASSWORD, constant.MyAccount.ENC_PASSWORD, 0, False)

            while session.IsLogin is False:
                pythoncom.PumpWaitingMessages( )

            XAQuery.t8413_event = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQuery)
            XAQuery.t8413_event.ResFileName = "/Res/t8413.res"

            Main.t8413_주식차트일주월(shcode="005930", gubun="3", qrycnt=500, sdate="", edate="99999999", cts_date="",
                               comp_yn="N", IsNext=False)

    @staticmethod
    def t8413_주식차트일주월(shcode=None, gubun=None, qrycnt=None, sdate=None, edate=None, cts_date=None, comp_yn=None,
                      IsNext=None):
        time.sleep(3.3)
        XAQuery.t8413_event.SetFieldData("t8413InBlock", "shcode", 0, shcode)
        XAQuery.t8413_event.SetFieldData("t8413InBlock", "gubun", 0, gubun)
        XAQuery.t8413_event.SetFieldData("t8413InBlock", "qrycnt", 0, qrycnt)
        XAQuery.t8413_event.SetFieldData("t8413InBlock", "sdate", 0, sdate)
        XAQuery.t8413_event.SetFieldData("t8413InBlock", "edate", 0, edate)
        XAQuery.t8413_event.SetFieldData("t8413InBlock", "cts_date", 0, cts_date)
        XAQuery.t8413_event.SetFieldData("t8413InBlock", "comp_yn", 0, comp_yn)
        XAQuery.t8413_event.Request(IsNext)

        XAQuery.t8413_IsOk = False
        while XAQuery.t8413_IsOk is False:
            pythoncom.PumpWaitingMessages( )


if __name__ == '__main__':
    Main( )
