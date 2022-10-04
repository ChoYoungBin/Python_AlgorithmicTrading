import win32com.client
import constant.MyAccount as MyAccount
import pythoncom


class XASession:
    IsLogin = False

    def OnLogin(self, code, message):
        if code == '0000':
            XASession.IsLogin = True
            print("로그인성공 = %s" % message)
        else:
            XASession.IsLogin = False

    def OnReceiveMessage(self, systemError, messageCode, message):
        pass


class LogIn:
    Id = MyAccount.ID
    Password = MyAccount.PASSWORD
    EncPassword = MyAccount.ENC_PASSWORD
    PRD_URL = MyAccount.PRD_SERVER_URL
    PRD_PORT = 20001

    def logIn(self):
        session = win32com.client.DispatchWithEvents("XA_Session.XASession", XASession)
        # Session연결 (URL + PORT)
        session.ConnectServer(self.PRD_URL, self.PRD_PORT)
        if session.IsConnected( ) is True:
            session.Login(self.Id, self.Password, self.EncPassword, 0, False)

            while XASession.IsLogin is False:
                pythoncom.PumpWaitingMessages( )
        else:
            session.Logout( )
            # Session 로그인
        return session


if __name__ == '__main__':
    mainObj = LogIn()
    mainObj.logIn()
