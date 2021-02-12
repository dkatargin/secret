import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import settings


class AESCipher(object):
    def __init__(self):
        self.bs = AES.block_size
        self.key = hashlib.sha256(settings.APP_SECRET.encode()).digest()

    def encrypt(self, plain_text):
        cipher = AES.new(self.key, AES.MODE_CBC)
        cipher_text = cipher.iv + cipher.encrypt(pad(plain_text.encode(), AES.block_size))
        cipher_text = base64.b64encode(cipher_text)
        return cipher_text.decode("UTF-8")

    def decrypt(self, data):
        decoded_enc = base64.b64decode(data)
        iv = decoded_enc[:16]
        cipher_text = decoded_enc[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        plain_text = unpad(cipher.decrypt(cipher_text), AES.block_size).decode("utf-8")
        return plain_text
