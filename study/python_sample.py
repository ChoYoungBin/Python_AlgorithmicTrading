# print("내용") # 문자 String , str
# print(35000) # 숫자 Integer, int
# print(3.5) # 실수 Float, float
# print(False) # Boolean
#
# 변수명 = '삼성전자'
# 변수명2 = 'LG전자'
# print("첫번째 %s, 두번째 %s" % (변수명, 변수명2))
#
# stock_price = 5000
# stock_price2 = 7000
# stock_plus = stock_price % stock_price2
# print("주식가격 더하기 %s" % stock_plus)
#
# if stock_plus > 5000:
#     print("5000이상이네 %s" % stock_plus)
# elif stock_plus == 5000:
#     print("뭐라구? %s" % stock_plus)
# else:
#     print("에라이")
#
# if (stock_plus > stock_price2) or (stock_plus < stock_price2):
#     print('ㅋㅋ')
#
#
# def setData(price: int = 3000, quantity: int = 10, name: str = None):
#     result = price * quantity
#     print('가격 %s, 수량 %s' % (price, quantity))
#
#     return result
#
#
# print(setData(price=20, quantity=10))
#
#
# def myData(myName: str = "", age: int = 0, address: str = "서울시"):
#     print("내 이름은 %s이고, 나이는 %s , 그리고 %s에 살아요" % (myName, age, address))
#
#     return "끝~!", 5, 10
#
#
# print(myData(myName="ㅋㅋㅋ", address="행복시"))


# class XingAPI( ):
#     stock_Name = "삼성"
#
#     def buy_calcul(self):
#         print("매수계산 함수")
#
#     # 생성자
#     def __init__(self):
#         self.num3 = None
#         print("class 초기화")
#         print(dir(self))
#         self.stock_Price = None
#         self.stock_Drate = None
#
#     def buy_fnc(self, num1):
#         num2 = 5
#         self.num3 = num1+num2
#         print(self.num3)
#
#
# mXingAPI = XingAPI( )
# result = mXingAPI.stock_Name
# print(result)
# mXingAPI.buy_calcul( );
# mXingAPI.buy_fnc(13)
#
# class XASession( ):
#
#     def OnLogin(self):
#         print("로그인 요청에 대한 수신")
#
#
# class Main( ):
#     def __init__(self):
#         print("Main Class. 증권 프로그램 초기세팅")
#
#     print("로그인요청 한다")
#     print("XASession 클래스에서 로그인 결과를 수신한다")
#     xa = XASession( )
#     xa.OnLogin( )
#
#
# if __name__ == '__main__':
#     Main( )

# # List
# 계좌목록 = ['삼성전자', 'LG전자', 'SK하이닉스']
# # Tuple
# tuple_sample = ("APPLE", "KAKAO", "NUMBER")
# for 계좌 in 계좌목록:
#     print(계좌)
#
# for 해외 in tuple_sample:
#     print(해외)
#
# 계좌목록.append("현대차")
# print(계좌목록[2])
#
# del 계좌목록[1]
# print(계좌목록[2])
#
# dict_sample = {"삼성전자": 10000, "카카오": 5000}
# print(dict_sample["카카오"])
#
# dict_sample["삼성전자"] = 100000
# print(dict_sample)
#
# del dict_sample["삼성전자"]
# print(dict_sample)
#
# multiple_sample = {"삼성전자": {"현재가": 100000, "등락률": 3.9, "내가산종목여부": False},
#                    "카카오": {"현재가": 5000, "등락률": 1.9, "내가산종목여부": True}}
#
# multiple_sample["카카오"]["거래량"] = 1000000
# del multiple_sample["카카오"]["등락률"]
# multiple_sample["LG"] = {"현재가": 3000}
# print(multiple_sample)

# sample_list = ["삼성", "LG", "카카오"]
# for name in sample_list:
#     print(name)
#
# sample = {"삼성": 10000, "LG": 2000, "카카오": 7000}
# sampleList = sample.keys( )
# for key in sampleList:
#     print(sample[key])
#     if key == "LG":
#         print("%s 인 것 확인됨. " % key)
#         break


test_list = list(range(5))
print(test_list)
for i in range(5):
    print("sample %s" % i)
