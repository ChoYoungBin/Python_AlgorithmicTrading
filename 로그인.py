import pythoncom
import win32com.client
from constant.MyAccount import PRD_SERVER_URL, PASSWORD, ID, ENC_PASSWORD


class XAQuery:
    def Login(self, code, message):
        pass


class XASession:
    IsLogin = False

    def OnLogin(self, code, message):
        print("loginCode = %s" % code)
        XASession.IsLogin = True


class Main:
    def __init__(self):
        self.password = PASSWORD
        self.id = ID

    def start(self):
        session = win32com.client.DispatchWithEvents("XA_Session.XASession", XASession)
        session.ConnectServer(PRD_SERVER_URL, 20001)

        if session.IsConnected( ) is True:
            session.Login(ID, PASSWORD, ENC_PASSWORD, 0, False)
            while XASession.IsLogin is False:
                pythoncom.PumpWaitingMessages( )
        else:
            session.DisconnectServer( )


if __name__ == '__main__':
    main_obj = Main( )
    main_obj.start( )
