import requests
import json


def buildHeaders(token):
    return {"Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "CHANNELID": "UX",
            "MYTELKOMSEL-MOBILE-APP-VERSION": "4.5.0"}


class UX:
    def __init__(self):
        self.msisdn: str
        self.token4: str
        self.signtrans: str

    def login(self):
        self.msisdn = input("Masukkan nomor Telkomsel (628xx): ")
        self.getOTP()

    def getOTP(self):
        print("Sedang mengirim kode OTP ke nomor tujuan...")
        requests.post("https://tdwidm.telkomsel.com/passwordless/start",
                      headers={"Content-Type": "application/x-www-form-urlencoded"},
                      data={"connection": "sms",
                            "phone_number": "+" + self.msisdn})
        print("Kode OTP telah dikirim.")
        self.getToken1()

    def getToken1(self):
        otp = input("Masukkan OTP: ")
        print("Mendapatkan token [1/4]...")
        response = requests.post("https://tdwidm.telkomsel.com/oauth/ro",
                                 headers={"Content-Type": "application/x-www-form-urlencoded"},
                                 data={"client_id": "TFKYtPumTXcLM8xEZATlvceX2Vtblaw3",
                                       "connection": "sms",
                                       "grant_type": "password",
                                       "username": "+" + self.msisdn,
                                       "password": otp,
                                       "scope": "openid offline_access",
                                       "device": "string"})

        try:
            token1 = response.json()["id_token"]
        except:
            print("OTP salah, silahkan coba lagi.")
            self.getToken1()
        self.getToken2(token1)

    def getToken2(self, token1):
        print("Mendapatkan token [2/4]...")
        response = requests.patch("https://tdw.telkomsel.com/api/user/",
                                  headers=buildHeaders(token1),
                                  data=json.dumps({"msisdn": self.msisdn,
                                                   "fingerPrint": "931b95c36ea89b36"}))
        self.getToken3(response.headers["Authorization"].replace("Bearer ", ""))

    def getToken3(self, token2):
        print("Mendapatkan token [3/4]...")
        response = requests.get("https://tdw.telkomsel.com/api/subscriber/v5/profile?msisdn=" + self.msisdn,
                                headers=buildHeaders(token2))

        self.getToken4(response.headers["Authorization"].replace("Bearer ", ""))

    def getToken4(self, token3):
        print("Mendapatkan token [4/4]...")
        response = requests.get("https://tdw.telkomsel.com/api/subscriber/hvc/information",
                                headers=buildHeaders(token3))

        self.token4 = response.headers["Authorization"].replace("Bearer ", "")
        self.getSigntrans(self.token4)

    def getSigntrans(self, token4):
        print("Mendapatkan signtrans...")
        response = requests.get("https://tdw.telkomsel.com/api/offers/filtered-offers/v3?filteredby=boid|ML2_BP_15&html=true",
                                headers=buildHeaders(token4))

        self.signtrans = response.headers["signtrans"]

    def buyPackage(self, pkgid):
        print("Membeli paket...")
        headers = buildHeaders(self.token4)
        headers["SIGNTRANS"] = self.signtrans

        response = requests.put("https://tdw.telkomsel.com/api/offers/v2/" + pkgid,
                                headers=headers,
                                data=json.dumps({"toBeSubscribedTo": False,
                                                 "paymentMethod": "AIRTIME"}))

        print(response.text)


def main():
    print("Telkomsel API UX (MyTelkomsel) v1.0")
    print("By      : Agung Watanabe (uragiristereo)")
    print("Github  : https://github.com/uragiristereo")
    print("Facebook: https://facebook.com/agutenx")
    myUX = UX()
    myUX.login()
    pkgid = input("Masukkan Package ID: ")
    myUX.buyPackage(pkgid)


if __name__ == "__main__":
    main()
