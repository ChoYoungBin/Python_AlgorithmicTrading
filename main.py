import time

import pythoncom
import win32com.client

from constant import MyAccount
from constant.MyAccount import PRD_SERVER_URL, ACCOUNT_PASSWORD, ACCOUNT_NUMBER


class XAQuery:
    acc_num = None
    # 잔고조회
    t0424_ok = False
    t0424_event = None

    # 계좌조회
    CSPAQ12200_ok = False
    CSPAQ12200_event = None
    # 종목조회
    t1452_event = None
    t1452_ok = False
    t1452_idx = ""

    mySource = {}

    # XAQuery 수신 callback Method
    def OnReceiveData(self, szCode):
        if szCode == "CSPAQ12200":
            print('수신완료 %s' % szCode)
            AbleAmount = self.CSPAQ12200_event.GetFieldData("CSPAQ12200OutBlock2", "MnyoutAbleAmt", 0)
            print("가능금액 %s" % AbleAmount)

        elif szCode == "t1452":
            print('수신완료 %s' % szCode)
            count = self.t1452_event.GetBlockCount("t1452OutBlock1")
            print("받은 갯수 %s" % count)
            t1452_idx = self.t1452_event.GetFieldData("t1452OutBlock", "idx", 0)
            indexCount = len(self.mySource.keys( ))

            for index in range(count):
                source = {}
                hname = self.t1452_event.GetFieldData("t1452OutBlock1", "hname", index)
                price = self.t1452_event.GetFieldData("t1452OutBlock1", "price", index)
                source["종목"] = hname
                source["가격"] = price
                self.mySource[str(indexCount + index)] = source

            print("ISNEXT ? %s" % self.t1452_event.IsNext)
            if self.t1452_event.IsNext is True:
                Main.GetMostVolumeList(index=t1452_idx, IsNext=self.t1452_event.IsNext)
            else:
                print(self.mySource)
                XAQuery.t1452_ok = True

        elif szCode == "t0424":
            cts_expcode = self.t0424_event.GetFieldData("t0424OutBlock", "cts_expcode", 0)
            print("CTS_EXPCODE =%s" % cts_expcode)
            cnt = self.t0424_event.GetBlockCount("t0424OutBlock1")
            print("현재 cnt 는 %s" % cnt)
            for idx in range(cnt):
                self.t0424_event.GetFieldData("t0424OutBlock1", "expcode", idx)
                self.t0424_event.GetFieldData("t0424OutBlock1", "mdposqt", idx)

            if self.IsNext is True:
                Main.주식잔고2(계좌번호=XAQuery.acc_num, cts_expcode=cts_expcode, IsNext=self.IsNext)
            else:
                XAQuery.t0424_ok = True


class XASession:
    # Class 변수
    login_ok = False

    def OnLogin(self, szCode, szMsg):
        # self.변수 => 인스턴스 변수

        print("%s %s" % (szCode, szMsg))

        if szCode == "0000":
            XASession.login_ok = True
        else:
            XASession.login_ok = False

    def OnReceiveMessage(self, systemError, messageCode, message):
        print("SystemError: %s, messageCode: %s, message : %s" % (systemError, messageCode, message))

    # 실행용 클래스


class Main:
    def __init__(self):
        print("클래스 실행")

    def start(self):
        # XA_Session , XA_Query, XA_Real
        mySession = self.processLogin( )

        myAccount = self.getMyAccounts(mySession)

        Main.GetMostVolumeList(myAccount)

    def getMyAccounts(self, session):
        # XAQuery => 단건 조회용
        XAQuery.CSPAQ12200_event = self.GetXAQuery( )
        XAQuery.CSPAQ12200_event.ResFileName = "/Res/CSPAQ12200_1.res"
        count = session.GetAccountListCount( )
        # range(5) => [0,1,2,3,4] 의 list 형태로 반환
        for account in range(count):
            szAcct = session.GetAccountList(account)
            print(szAcct)
            if szAcct == ACCOUNT_NUMBER:
                XAQuery.acc_num = szAcct
                print(XAQuery.acc_num)
                Main.주식잔고2(XAQuery.acc_num, XAQuery, False)
                # self.GetAvailableDeposit(szAcct)

    @staticmethod
    def 주식잔고2(계좌번호=None, cts_expcode="", IsNext=False):

        time.sleep(0.51)
        print("하이 계좌번호 = %s" % 계좌번호)
        XAQuery.t0424_event = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQuery)
        XAQuery.t0424_event.ResFileName = "/Res/t0424.res"
        print("하이2")
        XAQuery.t0424_event.SetFieldData("t0424InBlock", "accno", 0, 계좌번호)
        XAQuery.t0424_event.SetFieldData("t0424InBlock", "passwd", 0, ACCOUNT_PASSWORD)

        XAQuery.t0424_event.SetFieldData("t0424InBlock", "prcgb", 0, "1")
        XAQuery.t0424_event.SetFieldData("t0424InBlock", "chegb", 0, "2")
        XAQuery.t0424_event.SetFieldData("t0424InBlock", "dangb", 0, "0")
        XAQuery.t0424_event.SetFieldData("t0424InBlock", "charge", 0, "1")
        XAQuery.t0424_event.SetFieldData("t0424InBlock", "cts_expcode", 0, cts_expcode)
        print("하이3")
        XAQuery.t0424_event.Request(IsNext)

        XAQuery.t0424_ok = False
        while XAQuery.t0424_ok is False:
            pythoncom.PumpWaitingMessages( )

    # 로그인처리
    def processLogin(self):
        session = self.GetXASession( )
        session.ConnectServer(PRD_SERVER_URL, 20001)
        session.Login(MyAccount.ID, MyAccount.PASSWORD, MyAccount.ENC_PASSWORD, 0, False)
        while XASession.login_ok is False:
            pythoncom.PumpWaitingMessages( )
        return session

    # XASession 가져오기
    def GetXASession(self):
        return win32com.client.DispatchWithEvents("XA_Session.XASession", XASession)

    # XAQuery 가져오기
    def GetXAQuery(self):
        return win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQuery)

    def GetAvailableDeposit(self, account=None):

        time.sleep(5.1)
        XAQuery.CSPAQ12200_event.SetFieldData("CSPAQ12200InBlock1", "RecCnt", 0, 1)
        XAQuery.CSPAQ12200_event.SetFieldData("CSPAQ12200InBlock1", "MgmtBrnNo", 0, "")
        XAQuery.CSPAQ12200_event.SetFieldData("CSPAQ12200InBlock1", "AcntNo", 0, account)
        XAQuery.CSPAQ12200_event.SetFieldData("CSPAQ12200InBlock1", "Pwd", 0, ACCOUNT_PASSWORD)
        XAQuery.CSPAQ12200_event.SetFieldData("CSPAQ12200InBlock1", "BalCreTp", 0, "0")

        XAQuery.CSPAQ12200_event.Request(False)

        XAQuery.CSPAQ12200_ok = False
        while XAQuery.CSPAQ12200_ok is False:
            # 결과가 올때까지 대기
            pythoncom.PumpWaitingMessages( )

    @staticmethod
    def GetMostVolumeList(index="", IsNext=False):
        time.sleep(0.1)
        print("목록시작 index = %s" % index)
        XAQuery.t1452_event = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQuery)
        XAQuery.t1452_event.ResFileName = "/Res/t1452_2.res"
        XAQuery.t1452_event.SetFieldData("t1452InBlock", "gubun", 0, "1")
        XAQuery.t1452_event.SetFieldData("t1452InBlock", "jnilgubun", 0, "0")
        XAQuery.t1452_event.SetFieldData("t1452InBlock", "idx", 0, index)

        XAQuery.t1452_event.Request(IsNext)

        XAQuery.t1452_ok = False
        while XAQuery.t1452_ok is False:
            pythoncom.PumpWaitingMessages( )

    # TR목록 : 1:1 요청
    # REAL목록 : 1대:n요청 (한 번 요청하면 계속 수신 됨)


if __name__ == '__main__':
    main_obj = Main( )
    main_obj.start( )
