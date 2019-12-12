import requests
import json


def buildHeaders(token):
    return {"Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "CHANNELID": "VMP"}


class VMP:
    def __init__(self):
        self.msisdn: str
        self.token2: str

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
        print("Mendapatkan token [1/2]...")
        response = requests.post("https://tdwidm.telkomsel.com/oauth/ro",
                                 headers={"Content-Type": "application/x-www-form-urlencoded"},
                                 data={"client_id": "9yUwRUZirC0DXZyjMeQF4zCr6KO2R0Ub",
                                       "connection": "sms",
                                       "grant_type": "password",
                                       "username": "+" + self.msisdn,
                                       "password": otp,
                                       "scope": "openid offline_access",
                                       "device": "string"})

        try:
            token1 = response.json()["id_token"]
            self.getToken2(token1)
        except:
            print("OTP salah, silahkan coba lagi.")
            self.getToken1()

    def getToken2(self, token1):
        print("Mendapatkan token [2/2]...")
        response = requests.patch("https://vmp.telkomsel.com/api/user/",
                                  headers=buildHeaders(token1),
                                  data=json.dumps({"msisdn": self.msisdn}))

        self.token2 = response.json()["promotedToken"]

    def buyPackage(self, pkgid):
        print("Membeli paket...")
        response = requests.put("https://vmp.telkomsel.com/api/packages/" + pkgid,
                                headers=buildHeaders(self.token2),
                                data=json.dumps({"toBeSubscribedTo": False}))

        print(response.text)


def main():
    print("Telkomsel API VMP (MAXstream) v1.0")
    print("By      : Agung Watanabe (uragiristereo)")
    print("Github  : https://github.com/uragiristereo")
    print("Facebook: https://facebook.com/agutenx")
    myVMP = VMP()
    myVMP.login()
    pkgid = input("Masukkan Package ID: ")
    myVMP.buyPackage(pkgid)


if __name__ == "__main__":
    main()
